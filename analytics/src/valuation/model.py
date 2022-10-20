from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Valuation(BaseModel):
    pub_id: UUID = Field(default_factory=uuid4)
    task_id: UUID
    reward: int
    penalty: int


class ValuationInDB(Valuation):
    id: UUID = Field(default_factory=uuid4)

