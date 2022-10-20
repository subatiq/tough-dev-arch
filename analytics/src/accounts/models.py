from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Account(BaseModel):
    public_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    value: int = 0
    
    def reset(self) -> None: 
        self.value = 0


class AccountInDB(Account):
    id: UUID = Field(default_factory=uuid4)


