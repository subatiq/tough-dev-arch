from uuid import UUID
from src.event import Event


class UserCreated(Event):
    pub_id: UUID
    username: str
    email: str


