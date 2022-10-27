import random
from src.accounts.repo import AccountsRepository
from src.accounts.services import penalize_user, reward_user
from src.tasks.events import AssigneeShuffled, TaskAdded, TaskCompleted
from src.valuation.repo import ValuationsRepository
from src.valuation.model import Valuation


def handle_user_reward(acc_repo: AccountsRepository, val_repo: ValuationsRepository, event: TaskCompleted):
    print('REWARDING')
    reward_user(acc_repo, val_repo, event.body.assignee_id, event.body.task_id)


def handle_user_penalty(acc_repo: AccountsRepository, val_repo: ValuationsRepository, event: AssigneeShuffled):
    print('PANALTY')
    penalize_user(acc_repo, val_repo, event.body.assignee_id, event.body.task_id)


def handle_task_added(acc_repo: AccountsRepository, val_repo: ValuationsRepository, event: TaskAdded):
    print('ADDING')
    val_repo.save(Valuation(task_id=event.body.task_id, reward=random.randint(20, 40), penalty=random.randint(10, 20)))
    print(val_repo.get(event.body.task_id))
    print('=' * 30)
    print('=' * 30)
    print('=' * 30)
    penalize_user(acc_repo, val_repo, event.body.assignee_id, event.body.task_id)
