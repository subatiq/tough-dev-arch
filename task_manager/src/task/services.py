import random
from uuid import UUID
from src.common.broker import publish
from src.task.model import Task, TaskStatus
from src.task.repository import TaskNotFound, TaskRepository
from src.task.events import AssigneeChanged, NewTaskCreated, TaskAssigneeUpdated, TaskCompleted, TaskCreated, TaskStatusUpdatedToCompleted
from src.users.repo import UsersRepository


def create_task(tasks_repo: TaskRepository, users_repo: UsersRepository, title: str, description: str, assignee: UUID) -> UUID:
    if not users_repo.developers():
        raise ValueError("No developers registered")

    task = Task(
        title=title, 
        description=description, 
        assignee=assignee
    )
    tasks_repo.add(task)

    publish(
        "task.creation", 
        TaskCreated(task_id=task.id, assignee_id=random.choice(users_repo.developers()).pub_id)
    )
    publish(
        "tasks",
        NewTaskCreated(**task.dict())
    )

    return task.id


def complete_task(repo: TaskRepository, task_id: UUID):
    repo.set_status(task_id, TaskStatus.DONE)
    task = repo.get(task_id)

    if task is None:
        raise TaskNotFound(task_id)

    publish(
        "task.assignment",
        TaskCompleted(task_id=task_id, assignee_id=task.assignee)
    )
    publish(
        "tasks",
        TaskStatusUpdatedToCompleted(task_id=task_id)
    )


def assign_task(repo: TaskRepository, task_id: UUID, assignee_id: UUID):
    repo.assign(task_id, assignee_id)

    publish(
        "task.reassigned",
        AssigneeChanged(task_id=task_id, assignee_id=assignee_id)
    )
    publish(
        "tasks",
        TaskAssigneeUpdated(task_id=task_id, assignee_id=assignee_id)
    )

