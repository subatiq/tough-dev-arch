from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from src.users.model import User, UserRole


class UsersRepository(ABC):
    @abstractmethod
    def user(self, user_id: UUID):
        pass

    @abstractmethod
    def save(self, user: User):
        pass

    @abstractmethod
    def developers(self) -> list[User]:
        pass

class InMemoryUserRepository(UsersRepository):
    def __init__(self) -> None:
        user = User(username="subatiq", email="test@test.com", role = UserRole.DEVELOPER)
        self.users: dict[UUID, User] = {
            user.id: user
        }


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

    def developers(self) -> Sequence[User]:
        return [user for user in self.all() if user.role == UserRole.DEVELOPER]
