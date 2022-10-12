from uuid import UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.users.handlers import save_user
from src.common.broker import subscribe
from src.task.model import Task

from src.task.repository import InMemoryRepository, TaskNotFound
import src.task.services as services
from src.users.events import UserCreated
from src.users.repo import InMemoryUserRepository

app = FastAPI()
tokens_repo = InMemoryRepository()
users_repo = InMemoryUserRepository()


subscribe("user.created", UserCreated, save_user, kwargs={"repo": users_repo})


@app.get("/")
def read_root():
    return "Task manager"


@app.get("/tasks/{task_id}", response_model=Task)
def read_item(task_id: UUID):
    try:
        task = tokens_repo.get(task_id)
        return task
    except TaskNotFound:
        pass
    print(1)

    return HTTPException(status_code=404, detail=str(TaskNotFound))


@app.post("/tasks/complete/{task_id}")
def complete_task(task_id: UUID):
    services.complete_task(tokens_repo, task_id)
    return "OK"


class NewTaskInfo(BaseModel):
    title: str
    description: str
    assignee: UUID


@app.post("/tasks/create")
def create_task(task_info: NewTaskInfo):
    return services.create_task(tokens_repo, **task_info.dict())


class NewAssigneeInfo(BaseModel):
    assignee: UUID


@app.post("/tasks/assign/{task_id}")
def assign_task(task_id: UUID, assignee_info: NewAssigneeInfo):
    services.assign_task(tokens_repo, task_id, assignee_info.assignee)
    return "OK"


@app.get("/debug/users")
def all_users():
    return users_repo.all()
