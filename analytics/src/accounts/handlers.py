from src.accounts.events import AccountUpdated
from src.accounts.repo import InMemoryAccountsRepository
from src.valuation.events import ValuationCreated, ValuationUpdated
from src.valuation.repo import ValuationsRepository


def save_account(repo: InMemoryAccountsRepository, event: AccountUpdated):
    repo.save(event.body)


def save_valuation(repo: ValuationsRepository, event: ValuationCreated | ValuationUpdated):
    repo.save(event.body)
