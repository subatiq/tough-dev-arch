from abc import ABC, abstractmethod
from uuid import UUID
from src.accounts.models import AccountTransaction


class AccountsRepository(ABC):
    @abstractmethod
    def all_for_user(self, user_id: UUID) -> list[AccountTransaction]:
        pass

    @abstractmethod
    def last_user_transaction(self, user_id: UUID) -> AccountTransaction:
        pass

    @abstractmethod
    def last_billing_cycle(self, user_id: UUID) -> int:
        pass

    @abstractmethod
    def last_closing_transaction(self, user_id: UUID) -> AccountTransaction:
        pass

    @abstractmethod
    def balance(self, user_id: UUID) -> int:
        pass

    @abstractmethod
    def save(self, transaction: AccountTransaction):
        pass

    @abstractmethod
    def last_cycle_balance(self, user_id: UUID) -> int:
        pass


class InMemoryAccountsRepository(AccountsRepository):
    def __init__(self) -> None:
        self.log: list[AccountTransaction] = []

    def all_for_user(self, user_id: UUID) -> list[AccountTransaction]:
        return [transaction for transaction in self.log if transaction.user_id == user_id]

    def all_for_last_billing_cycle(self, user_id: UUID) -> list[AccountTransaction]:
        return [transaction for transaction in self.all_for_user(user_id) if transaction.billing_cycle == self.last_billing_cycle(user_id)]

    def last_user_transaction(self, user_id: UUID) -> AccountTransaction | None:
        users_transactions = self.all_for_user(user_id)
        return self.all_for_user(user_id)[-1] if len(users_transactions) > 0 else None

    def last_billing_cycle(self, user_id: UUID) -> int:
        transaction = self.last_user_transaction(user_id)
        if transaction is None:
            return 0
        return transaction.billing_cycle if not transaction.closing else transaction.billing_cycle + 1

    def last_closing_transaction(self, user_id: UUID) -> AccountTransaction:
        return [transaction for transaction in self.all_for_user(user_id) if transaction.closing][-1]

    def last_cycle_balance(self, user_id: UUID) -> int:
        return self.last_closing_transaction(user_id).credit

    def save(self, transaction: AccountTransaction):
        transaction.billing_cycle = self.last_billing_cycle(transaction.user_id)
        self.log.append(transaction)

    def balance(self, user_id: UUID) -> int:
        debit = [transaction.debit for transaction in self.all_for_last_billing_cycle(user_id)]
        credit = [transaction.credit for transaction in self.all_for_last_billing_cycle(user_id)]
        print('DEBIT')

        return sum(debit) - sum(credit)
