from src.accounts.events import AccountCreated, AccountUpdated
from src.accounts.repo import InMemoryAccountsRepository


def save_account(repo: InMemoryAccountsRepository, event: AccountCreated | AccountUpdated):
    repo.save(event.body)

