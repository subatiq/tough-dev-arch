from fastapi import FastAPI
from brokereg import subscribe
from src.accounts.handlers import handle_user_registration
from src.accounts.handlers import handle_user_penalty
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
    users_events.UserUpdated, save_user, kwargs={"repo": users_repo}
)

subscribe(
    [users_events.REGISTRATION_FLOW],
    users_events.UserRegistered,
    handle_user_registration,
    kwargs={"acc_repo": accounts_repo})


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


subscribe(
    [users_events.USER_CREATED],
    users_events.UserCreated, save_user, kwargs={"repo": users_repo}
)


@app.get("/")
def read_root():
    return "Accounting service"

