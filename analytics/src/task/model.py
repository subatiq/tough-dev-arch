from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, Field


class TaskStatus(Enum):
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    pub_id: UUID
    created_at: datetime
    completed_at: datetime
    title: str
    description: str
    assignee: UUID
    status: TaskStatus



