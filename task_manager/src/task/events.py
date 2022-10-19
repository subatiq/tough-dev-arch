from uuid import UUID
from brokereg import Event
from brokereg.event import EventData
from pydantic import BaseModel

from src.task.model import Task


BE_DOMAIN = 'task-lifecycle'
CUD_DOMAIN = 'task-streaming'


class TaskManagerEvent(Event):
    producer: str = "task_manager"
    domain: str = BE_DOMAIN


class TaskAddedData(EventData):
    task_id: UUID
    assignee_id: UUID


class TaskAdded(TaskManagerEvent):
    name: str = "TaskAdded"
    version: int = 1
    body: TaskAddedData


class TaskCompletedData(BaseModel):
    task_id: UUID
    assignee_id: UUID


class TaskCompleted(TaskManagerEvent):
    name: str = "TaskCompleted"
    version: int = 1
    body: TaskCompletedData


class AssigneeShuffledData(EventData):
    task_id: UUID
    assignee_id: UUID


class AssigneeShuffled(TaskManagerEvent):
    name: str = "AssigneeShuffled"
    version: int = 1
    body: AssigneeShuffledData


# CUDs


class TaskCUDEvent(TaskManagerEvent):
    body: Task


class TaskUpdated(TaskCUDEvent):
    domain: str = CUD_DOMAIN + '.updated'
    name: str = 'TaskUpdated'
    version: int = 1


class TaskCreated(TaskCUDEvent):
    domain: str = CUD_DOMAIN + '.created'
    name: str = 'TaskCreated'
    version: int = 1

