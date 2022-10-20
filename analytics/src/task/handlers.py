from src.task.events import TaskCreated, TaskUpdated
from src.task.repository import TaskRepository


def save_task(repo: TaskRepository, event: TaskCreated | TaskUpdated):
    repo.add(event.body)

