from uuid import UUID
from src.task.model import Task, TaskStatus
from src.task.repository import TaskRepository


def create_task(repo: TaskRepository, title: str, description: str, assignee: UUID) -> UUID:
    task = Task(
        title=title, 
        description=description, 
        assignee=assignee
    )

    repo.add(task)
    return task.id


def complete_task(repo: TaskRepository, task_id: UUID):
    repo.set_status(task_id, TaskStatus.DONE)


def assign_task(repo: TaskRepository, task_id: UUID, assignee_id: UUID):
    repo.assign(task_id, assignee_id)

