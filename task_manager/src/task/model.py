from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TaskStatus(Enum):
    IN_PROGRESS = "in_progress"
    DONE = "done"


class _DeprecatedTask(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    pub_id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    assignee: UUID
    status: TaskStatus = TaskStatus.IN_PROGRESS


class Task(_DeprecatedTask):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None
    jira_id: str



