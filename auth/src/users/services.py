import hashlib
from pydantic import SecretStr
from src.common.broker import publish
from src.users.model import User, UserInDB
from src.users.events import NewUserCreated, UserCreated
from src.users.repo import UsersRepository


def login(user: UserInDB, password: SecretStr) -> bool:
    if user and user.password_hash == hashlib.md5(password.get_secret_value().encode()).digest():
        return True

    return False


def register(repo: UsersRepository, user: User, password: SecretStr):
    user = user.to_db(password)
    repo.register(user)
    publish("user.registration", UserCreated(**user.dict(exclude={"id"})))
    publish("user", NewUserCreated(**user.dict(exclude={"id"})))
