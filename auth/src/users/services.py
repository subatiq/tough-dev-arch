import hashlib
from pydantic import SecretStr
from brokereg import publish
from src.users.model import User, UserInDB
from src.users.events import UserCreated, UserRegistered, UserRegisteredData
from src.users.repo import UsersRepository


def login(user: UserInDB, password: SecretStr) -> bool:
    if user and user.password_hash == hashlib.md5(password.get_secret_value().encode()).digest():
        return True

    return False


def register(repo: UsersRepository, user: User, password: SecretStr):
    user = user.to_db(password)
    repo.register(user)

    event_data = UserRegisteredData(**user.dict())
    publish(UserRegistered(body=event_data))
    publish(UserCreated(body=user.to_public()))
