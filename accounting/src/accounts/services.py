from uuid import UUID

from brokereg import publish
from src.accounts.events import AccountUpdated, BillingCycleCompleted, BillingCycleCompletedData, UserGotPayed, UserGotPayedData
from src.accounts.models import AccountTransaction
from src.accounts.repo import AccountsRepository
from src.users.repo import UsersRepository
from src.valuation.repo import ValuationsRepository


def reward_user(acc_repo: AccountsRepository, val_repo: ValuationsRepository, user_id: UUID, task_id: UUID) -> None:
    task_valuation = val_repo.get(task_id)

    if task_valuation is None:
        raise ValueError(f"Valuation for task {task_id} not found")

    transaction = AccountTransaction(user_id=user_id, description=str(task_id), debit=task_valuation.reward)
    acc_repo.save(transaction)
    publish(AccountUpdated(body=transaction))


def penalize_user(acc_repo: AccountsRepository, val_repo: ValuationsRepository, user_id: UUID, task_id: UUID) -> None:
    task_valuation = val_repo.get(task_id)

    if task_valuation is None:
        raise ValueError(f"Valuation for task {task_id} not found")

    transaction = AccountTransaction(user_id=user_id, description=str(task_id), credit=task_valuation.penalty)
    acc_repo.save(transaction)
    publish(AccountUpdated(body=transaction))


def pay_user(acc_repo: AccountsRepository, user_id: UUID, amount: int) -> None:
    transaction = AccountTransaction(user_id=user_id, description=str('Pay out'), closing=True, credit=amount) 
    acc_repo.save(transaction)

    print(f"User {user_id} was payed {amount}")

    event_data = UserGotPayedData(user_id=user_id)
    publish(UserGotPayed(body=event_data))


def send_report(user_repo: UsersRepository, user_id: UUID, earned: int) -> None:
    user = user_repo.user(user_id)

    if user is None:
        raise ValueError(f"User {user_id} not found")

    print(f"SENDING REPORT TO {user.email}:\n\tEARNED {earned}")


def complete_billing_cycle(user_repo: UsersRepository, acc_repo: AccountsRepository, user_id: UUID) -> None:
    # Get latest balance
    print(f'CLOSING FOR {user_id}')
    user_balance = acc_repo.balance(user_id)
    print(f'BALANCE = {user_balance}')

    # Check if can be payed
    if user_balance > 0:
        # Pay out and close cycle in one transaction
        pay_user(acc_repo, user_id, user_balance)
    else:
        # Just close cycle without balance change
        transaction = AccountTransaction(user_id=user_id, description="Closing", closing=True)
        acc_repo.save(transaction)

        publish(AccountUpdated(body=transaction))


    send_report(user_repo, user_id, user_balance)

    publish(BillingCycleCompleted(body=BillingCycleCompletedData(user_id=user_id)))

