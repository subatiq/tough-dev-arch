from uuid import UUID
from src.accounts.models import Account
from src.accounts.repo import AccountsRepository
from src.users.repo import UsersRepository
from src.valuation.repo import ValuationsRepository


def create_account(acc_repo: AccountsRepository, user_id: UUID) -> None:
    account = Account(user_id=user_id)
    acc_repo.save(account)


def reward_user(acc_repo: AccountsRepository, val_repo: ValuationsRepository, user_id: UUID, task_id: UUID) -> None:
    account = acc_repo.get(user_id)

    if account is None:
        raise ValueError(f"Account for user {user_id} not found")
        

    task_valuation = val_repo.get(task_id)

    if task_valuation is None:
        raise ValueError(f"Valuation for task {task_id} not found")

    account.value += task_valuation.penalty


def penalize_user(acc_repo: AccountsRepository, val_repo: ValuationsRepository, user_id: UUID, task_id: UUID) -> None:
    account = acc_repo.get(user_id)

    if account is None:
        raise ValueError(f"Account for user {user_id} not found")

    task_valuation = val_repo.get(task_id)

    if task_valuation is None:
        raise ValueError(f"Valuation for task {task_id} not found")

    account.value -= task_valuation.penalty


def pay_user(repo: AccountsRepository, user_id: UUID) -> int:
    account = repo.get(user_id)

    if account is None:
        raise ValueError(f"Account for user {user_id} not found")

    can_be_payed = account.value

    if can_be_payed > 0:
        account.reset()
        repo.save(account)

    return can_be_payed


def send_report(user_repo: UsersRepository, user_id: UUID, earned: int) -> None:
    user = user_repo.user(user_id)

    if user is None:
        raise ValueError(f"User {user_id} not found")

    print(f"SENDING REPORT TO {user.email}:\n\tEARNED {earned}")


def complete_billing_cycle(user_repo: UsersRepository, acc_repo: AccountsRepository, user_id: UUID) -> None:
    payed = pay_user(acc_repo, user_id)
    send_report(user_repo, user_id, payed)


