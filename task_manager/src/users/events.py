from uuid import UUID
from src.common.event import Event


class UserCreated(Event):
    pub_id: UUID
    username: str
    email: str


