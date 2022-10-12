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
