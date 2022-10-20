from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Account(BaseModel):
    public_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    value: int = 0
    
    def reset(self) -> None: 
        self.value = 0


class AccountTransaction(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    public_id: UUID = Field(default_factory=uuid4)
    billing_cycle: int = 0
    user_id: UUID
    credit: int = 0
    debit: int = 0
    description: str
    closing: bool = False


class AccountInDB(Account):
    id: UUID = Field(default_factory=uuid4)



