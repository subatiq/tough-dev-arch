import hashlib
from pydantic import SecretStr
from src.broker import publish
from src.users.model import User, UserInDB
from src.users.events import UserCreated
from src.users.repo import UsersRepository


def login(user: UserInDB, password: SecretStr) -> bool:
    if user and user.password_hash == hashlib.md5(password.get_secret_value().encode()).digest():
        return True

    return False


def register(repo: UsersRepository, user: User, password: SecretStr):
    user = user.to_db(password)
    repo.register(user)
    publish("user.created", UserCreated(pub_id=user.id, username=user.username, email=user.email))
    print("SENT")
