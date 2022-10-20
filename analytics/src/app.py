from fastapi import FastAPI
from brokereg import subscribe
from accounts.handlers import save_account
from src.accounts.repo import InMemoryAccountsRepository
from src.task import events as tasks_events
from src.users import events as users_events
from src.users.repo import InMemoryUserRepository
from src.valuation import events as valuation_events
from src.valuation.repo import InMemoryValuationRepository
from task.handlers import save_task
from task.repository import InMemoryTasksRepository
from users.handlers import save_user
from src.accounts import events as accounts_events

app = FastAPI()

users_repo = InMemoryUserRepository()
tasks_repo = InMemoryTasksRepository()
accounts_repo = InMemoryAccountsRepository()
val_repo = InMemoryValuationRepository()


subscribe(
    [users_events.USER_CREATED],
    users_events.UserCreated, save_user, kwargs={"repo": users_repo}
)

subscribe(
    [tasks_events.TASK_CREATED],
    tasks_events.TaskCreated, save_task, kwargs={"repo": tasks_repo}
)

subscribe(
    [tasks_events.TASK_UPDATED],
    tasks_events.TaskUpdated, save_account, kwargs={"repo": tasks_repo}
)

subscribe(
    [accounts_events.ACCOUNT_CREATED],
    accounts_events.AccountCreated, save_account, kwargs={"repo": accounts_repo}
)

subscribe(
    [accounts_events.ACCOUNT_UPDATED],
    accounts_events.AccountUpdated, save_account, kwargs={"repo": accounts_repo}
)


subscribe(
    [tasks_events.LIFECYCLE_FLOW],
    tasks_events.TaskCompleted, 
    handle_user_reward, 
    kwargs={"acc_repo": accounts_repo, "val_repo": val_repo})


subscribe(
    [tasks_events.ASSIGNMENT_FLOW],
    tasks_events.AssigneeShuffled, 
    handle_user_penalty, 
    kwargs={"acc_repo": accounts_repo, "val_repo": val_repo})




@app.get("/")
def read_root():
    return "Accounting service"

