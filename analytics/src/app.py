from analytics.services import get_management_profit_today, get_most_valuable_task_for_last_days, get_users_in_debt
from fastapi import FastAPI, HTTPException
from brokereg import subscribe
from src.accounts.handlers import save_account, save_valuation
from src.task import events as tasks_events
from src.users import events as users_events
from src.accounts.repo import InMemoryAccountsRepository
from src.users.repo import InMemoryUserRepository
from src.valuation import events as valuation_events
from src.valuation.repo import InMemoryValuationRepository
from src.task.handlers import save_task
from src.task.repository import InMemoryTasksRepository
from src.users.handlers import save_user
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
    [accounts_events.ACCOUNT_UPDATED],
    accounts_events.AccountUpdated, save_account, kwargs={"repo": accounts_repo}
)

subscribe(
    [valuation_events.VALUATION_CREATED],
    valuation_events.ValuationCreated, save_valuation, kwargs={"repo": val_repo}
)


subscribe(
    [valuation_events.VALUATION_UPDATED],
    valuation_events.ValuationUpdated, save_valuation, kwargs={"repo": val_repo}
)

@app.get("/")
def read_root():
    return "Analytics service"


@app.get("/tasks/max_value")
def max_value_task(days: int):
    task, price = get_most_valuable_task_for_last_days(tasks_repo=tasks_repo, val_repo=val_repo, days=days)
    if task:
        return {"reward": price, **task.dict()}
    else:
        raise HTTPException(status_code=404, detail="No tasks completed in this interval")

@app.get("/users/in_debt")
def users_in_debt():
    return get_users_in_debt(users_repo, accounts_repo)


@app.get("/profits/management")
def management_profits():
    return get_management_profit_today(users_repo, accounts_repo)
