from abc import ABC, abstractmethod
import hashlib
from uuid import UUID

from src.users.model import UserInDB, UserRole


class UsersRepository(ABC):
    @abstractmethod
    def register(self, user: UserInDB):
        pass

    @abstractmethod
    def user(self, user_id: UUID):
        pass


class InMemoryUserRepository(UsersRepository):
    def __init__(self) -> None:
        self.users: dict[UUID, UserInDB] = {
            UUID("167062ac-2b28-441e-ad3f-88adda18fef8"): UserInDB(
                id=UUID("167062ac-2b28-441e-ad3f-88adda18fef8"),
                email="test@test.com",
                username="admin",
                password_hash=hashlib.md5('123456'.encode()).digest(),
                role=UserRole.ADMIN
            )
        }

    def register(self, user: UserInDB):
        self.users[user.id] = user

    def user(self, user_id: UUID) -> UserInDB | None:
        for user in self.users.values():
            if user.pub_id == user_id:
                return user

    def user_by_name(self, username: str) -> UserInDB | None:
        for user in self.users.values():
            if user.username == username:
                return user

        
