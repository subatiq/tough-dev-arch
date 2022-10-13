from uuid import UUID
from src.common.event import Event
from src.users.model import UserRole


class UserCreated(Event):
    pub_id: UUID
    username: str
    email: str
    role: UserRole


# CUDs

class NewUserCreated(UserCreated):
    pass

