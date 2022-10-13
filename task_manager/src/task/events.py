from uuid import UUID
from src.common.event import Event


class TaskCreated(Event):
    task_id: UUID
    assignee_id: UUID

class TaskCompleted(Event):
    task_id: UUID
    assignee_id: UUID

class AssigneeChanged(Event):
    task_id: UUID
    assignee_id: UUID


# CUDs

class TaskAssigneeUpdated(Event):
    task_id: UUID
    assignee_id: UUID


class TaskStatusUpdatedToCompleted(Event):
    task_id: UUID


class NewTaskCreated(Event):
    pub_id: UUID
    title:  str
    description: str
    assignee: UUID

