from uuid import UUID
from src.accounts.services import complete_billing_cycle
from fastapi import FastAPI
from brokereg import subscribe
from src.accounts.handlers import handle_task_added, handle_user_penalty
from src.accounts.handlers import handle_user_reward
from src.accounts.repo import InMemoryAccountsRepository
from src.tasks import events as tasks_events
from src.users import events as users_events
from src.users.handlers import save_user
from src.users.repo import InMemoryUserRepository
from src.valuation.repo import InMemoryValuationRepository

app = FastAPI()

users_repo = InMemoryUserRepository()
accounts_repo = InMemoryAccountsRepository()
val_repo = InMemoryValuationRepository()


subscribe(
    [users_events.USER_UPDATED], 
    {"UserUpdated": (users_events.UserUpdated, save_user, {"repo": users_repo})}
)
    


subscribe(
    [tasks_events.LIFECYCLE_FLOW],
    {
        "TaskAdded": (tasks_events.TaskAdded, handle_task_added, {"acc_repo": accounts_repo, "val_repo": val_repo}),
        "TaskCompleted": (tasks_events.TaskAdded, handle_user_reward, {"acc_repo": accounts_repo, "val_repo": val_repo})
    }
)


subscribe(
    [tasks_events.ASSIGNMENT_FLOW],
    {"AssigneeShuffled": (tasks_events.AssigneeShuffled, handle_user_penalty, {"acc_repo": accounts_repo, "val_repo": val_repo})})


subscribe(
    [users_events.USER_CREATED],
    {"UserCreated": (users_events.UserCreated, save_user, {"repo": users_repo})}
)


@app.get("/")
def read_root():
    return "Accounting service"


@app.post("/complete_billing_cycle")
def complete_bc():
    for user in users_repo.all():
        complete_billing_cycle(users_repo, accounts_repo, user.pub_id)


@app.get("/balance/{user_id}")
def balance(user_id: UUID):
    return accounts_repo.balance(user_id)


@app.get("/users/all")
def users():
    return users_repo.all()


@app.get("/transactions/{user_id}")
def transactions(user_id: UUID):
    return accounts_repo.all_for_user(user_id)

