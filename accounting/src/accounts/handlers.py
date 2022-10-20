from src.accounts.repo import AccountsRepository
from src.accounts.services import create_account, penalize_user, reward_user
from src.tasks.events import AssigneeShuffled, TaskCompleted
from src.users.events import UserRegistered
from src.valuation.repo import ValuationsRepository


def handle_user_reward(acc_repo: AccountsRepository, val_repo: ValuationsRepository, event: TaskCompleted):
    reward_user(acc_repo, val_repo, event.body.assignee_id, event.body.task_id)


def handle_user_penalty(acc_repo: AccountsRepository, val_repo: ValuationsRepository, event: AssigneeShuffled):
    penalize_user(acc_repo, val_repo, event.body.assignee_id, event.body.task_id)


def handle_user_registration(acc_repo: AccountsRepository, event: UserRegistered):
    create_account(acc_repo, event.body.pub_id)
    
