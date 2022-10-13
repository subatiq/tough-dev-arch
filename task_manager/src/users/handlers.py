from src.users.events import UserCreated
from src.users.repo import UsersRepository
from src.users.model import User


def save_user(repo: UsersRepository, event: UserCreated):
    repo.save(User(**event.dict()))
    print(repo.developers())

