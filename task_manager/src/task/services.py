from datetime import datetime
import random
from uuid import UUID
from brokereg import publish
from src.task.model import Task, TaskStatus
from src.task.repository import TaskNotFound, TaskRepository
from src.task.events import AssigneeShuffled, AssigneeShuffledData, TaskAdded, TaskAddedData, TaskCompleted, TaskCompletedData, TaskCreated, TaskUpdated, _DeprecatedTaskUpdated, _DeprecatedTaskCreated, _DeprecatedTask
from src.users.repo import UsersRepository


def check_jira_id_not_in_title(title: str):
    if '[' in title or ']' in title:
        raise ValueError("Stop putting jira ID, popug")


def create_task(tasks_repo: TaskRepository, users_repo: UsersRepository, title: str, jira_id: str, description: str, assignee: UUID) -> UUID:
    if not users_repo.developers():
        raise ValueError("No developers registered")
    
    # FIXME: Should be in Task init validator
    check_jira_id_not_in_title(title)

    task = Task(
        title=title, 
        jira_id=jira_id,
        description=description, 
        assignee=assignee
    )
    tasks_repo.add(task)

    event_data = TaskAddedData(task_id=task.id, assignee_id=random.choice(users_repo.developers()).pub_id)
    publish(TaskAdded(body=event_data))

    publish(TaskCreated(body=task))
    publish(_DeprecatedTaskCreated(body=_DeprecatedTask(**task.dict())))

    return task.id


def complete_task(repo: TaskRepository, task_id: UUID):
    repo.set_status(task_id, TaskStatus.DONE)
    task = repo.get(task_id)

    if task is None:
        raise TaskNotFound(task_id)

    task.completed_at = datetime.utcnow()
    repo.update_info(task)

    event_data = TaskCompletedData(task_id=task.id, assignee_id=task.assignee)
    publish(TaskCompleted(body=event_data))

    publish(TaskUpdated(body=task))
    publish(_DeprecatedTaskUpdated(body=_DeprecatedTask(**task.dict())))


def assign_tasks(repo: TaskRepository, users_repo: UsersRepository):
    for task in repo.all():
        assignee_id = random.choice(users_repo.developers()).pub_id
        repo.assign(task.id, assignee_id=assignee_id)

        event_data = AssigneeShuffledData(task_id=task.pub_id, assignee_id=assignee_id)
        publish(AssigneeShuffled(body=event_data))

        publish(TaskUpdated(body=task))
        publish(_DeprecatedTaskUpdated(body=_DeprecatedTask(**task.dict())))

