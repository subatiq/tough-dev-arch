from abc import ABC, abstractmethod
from uuid import UUID

from src.users.model import User


class UsersRepository(ABC):
    @abstractmethod
    def user(self, user_id: UUID):
        pass

    @abstractmethod
    def save(self, user: User):
        pass

class InMemoryUserRepository(UsersRepository):
    def __init__(self) -> None:
        self.users: dict[UUID, User] = {}


    def user(self, user_id: UUID) -> User | None:
        for user in self.users.values():
            if user.id == user_id:
                return user

    def user_by_name(self, username: str) -> User | None:
        for user in self.users.values():
            if user.username == username:
                return user

    def save(self, user: User):
        self.users[user.id] = user

        
    def all(self) -> list[User]:
        return list(self.users.values())
