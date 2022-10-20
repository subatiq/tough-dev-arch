from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, Field


class TaskStatus(Enum):
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(BaseModel):
    pub_id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    assignee: UUID
    status: TaskStatus = TaskStatus.IN_PROGRESS



