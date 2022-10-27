from datetime import datetime, timedelta
from src.accounts.repo import AccountsRepository
from src.task.model import Task
from src.task.repository import TaskRepository
from src.users.model import User
from src.users.repo import UsersRepository
from src.valuation.repo import ValuationsRepository


def get_management_profit_today(user_repo: UsersRepository, acc_repo: AccountsRepository) -> int:
    total = 0
    for user in user_repo.all():
        total += acc_repo.last_cycle_balance(user.pub_id)

    return total


def get_users_in_debt(user_repo: UsersRepository, acc_repo: AccountsRepository) -> list[User]:
    users_in_debt = []
    for user in user_repo.all():
        last_earnings = acc_repo.last_cycle_balance(user.pub_id)

        if last_earnings >= 0:
            continue

        users_in_debt.append(user)

    return users_in_debt


def get_most_valuable_task_for_last_days(
    tasks_repo: TaskRepository, 
    val_repo: ValuationsRepository, 
    days: int = 1
    ) -> tuple[Task | None, int]:
    max_reward = 0
    max_rewarded_task = None

    for task in [
            task 
            for task 
            in tasks_repo.completed() 
            if task.completed_at > datetime.now() - timedelta(days=days)
        ]:
        valuation = val_repo.get(task.id)
        if valuation is None:
            continue

        if valuation.reward > max_reward:
            max_reward = valuation.reward
            max_rewarded_task = task

    return max_rewarded_task, max_reward
        
