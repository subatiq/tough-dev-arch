from abc import ABC, abstractmethod
from uuid import UUID
from src.accounts.models import Account, AccountInDB


class AccountsRepository(ABC):
    @abstractmethod
    def get(self, task_id: UUID):
        pass

    @abstractmethod
    def save(self, account: Account):
        pass
		

class InMemoryAccountsRepository(AccountsRepository):
    def __init__(self) -> None:
        self.data: dict[UUID, AccountInDB] = {}

    def get(self, user_id: UUID) -> Account | None:
        for account in self.data.values():
            if account.user_id == user_id:
                return Account(**account.dict())

    def save(self, account: Account):
        db_val = AccountInDB(**account.dict())
        self.data[db_val.id] = db_val
