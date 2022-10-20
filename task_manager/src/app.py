import os
from uuid import UUID

from fastapi.responses import RedirectResponse
from httpx import post

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel
from src.users.handlers import save_user
from brokereg import subscribe
from src.task.model import Task

from src.task.repository import InMemoryRepository, TaskNotFound
import src.task.services as services
from src.users.events import USER_CREATED, UserCreated
from src.users.repo import InMemoryUserRepository
from src.users.model import UserRole

app = FastAPI()
tokens_repo = InMemoryRepository()
users_repo = InMemoryUserRepository()


subscribe(
    [USER_CREATED],
    UserCreated, save_user, kwargs={"repo": users_repo}
)


@app.get("/")
def read_root():
    return "Task manager"


@app.get("/tasks/{task_id}", response_model=Task)
def read_all(task_id: UUID):
    try:
        task = tokens_repo.get(task_id)
        return task
    except TaskNotFound:
        pass

    return HTTPException(status_code=404, detail=str(TaskNotFound))


@app.get("/tasks", response_model=list[Task])
def read_item():
    return list(tokens_repo.data.values())


def check_token(request: Request):
    print('Checking')
    access_token = request.headers['Authorization'].split(' ')[-1]
    print(access_token)
    auth_server = os.getenv("AUTH_SERVER", "localhost:5050")
    response = post(f'http://{auth_server}/authz', json={"access_token": access_token.split(' ')[-1]})
    print(response)
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return UserRole(response.json()["role"])


def redirect_to_auth():
    auth_server = os.getenv("AUTH_SERVER", "localhost:5050")
    return RedirectResponse(f'http://{auth_server}/login')



@app.post("/tasks/complete/{task_id}")
def complete_task(task_id: UUID, authz=Depends(check_token)):
    services.complete_task(tokens_repo, task_id)
    return "OK"


class NewTaskInfo(BaseModel):
    title: str
    description: str
    assignee: UUID


@app.post("/tasks/create")
def create_task(task_info: NewTaskInfo, authz=Depends(check_token)):
    return services.create_task(tokens_repo, users_repo, **task_info.dict())


class NewAssigneeInfo(BaseModel):
    assignee: UUID


@app.post("/tasks/reassign_all")
def assign_task(authz=Depends(check_token)):
    if authz not in {UserRole.ADMIN, UserRole.MANAGER}:
        raise HTTPException(status_code=403, detail="Your role does not allow that")

    services.assign_tasks(tokens_repo, users_repo)
    return "OK"


@app.get("/users")
def all_users():
    return users_repo.all()

