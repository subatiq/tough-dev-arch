from uuid import UUID
from brokereg import Event
from brokereg.event import EventData
from brokereg.common import cud_topic, CUD_Type
from pydantic import BaseModel

from src.task.model import Task


LIFECYCLE_FLOW = 'task-lifecycle'
ASSIGNMENT_FLOW = 'task-assignment'

CUD_AGGREGATE = 'task'

TASK_CREATED = cud_topic(CUD_AGGREGATE, CUD_Type.CREATED)
TASK_UPDATED = cud_topic(CUD_AGGREGATE, CUD_Type.UPDATED)



class TaskManagerEvent(Event):
    producer: str = "task_manager"


class TaskAddedData(EventData):
    task_id: UUID
    assignee_id: UUID


class TaskAdded(TaskManagerEvent):
    name: str = "TaskAdded"
    version: int = 1
    body: TaskAddedData
    domain: str = LIFECYCLE_FLOW


class TaskCompletedData(BaseModel):
    task_id: UUID
    assignee_id: UUID


class TaskCompleted(TaskManagerEvent):
    name: str = "TaskCompleted"
    version: int = 1
    body: TaskCompletedData
    domain: str = LIFECYCLE_FLOW


class AssigneeShuffledData(EventData):
    task_id: UUID
    assignee_id: UUID


class AssigneeShuffled(TaskManagerEvent):
    name: str = "AssigneeShuffled"
    version: int = 1
    body: AssigneeShuffledData
    domain: str = ASSIGNMENT_FLOW


# CUDs


class TaskCUDEvent(TaskManagerEvent):
    body: Task


class TaskUpdated(TaskCUDEvent):
    domain: str = TASK_UPDATED
    name: str = 'TaskUpdated'
    version: int = 1


class TaskCreated(TaskCUDEvent):
    domain: str = TASK_CREATED
    name: str = 'TaskCreated'
    version: int = 1

