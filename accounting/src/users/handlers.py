from src.users.events import UserCreated
from src.users.repo import UsersRepository


def save_user(repo: UsersRepository, event: UserCreated):
    repo.save(event.body)

