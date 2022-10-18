from uuid import UUID
from brokereg import Event, EventData
from src.users.model import User
from src.users.model import UserRole

BE_DOMAIN = "user-registration"
CUD_DOMAIN = 'user-streaming'

class AuthEvent(Event):
    producer: str = "auth"


class UserRegisteredData(EventData):
    pub_id: UUID
    username: str
    email: str
    role: UserRole


class UserRegistered(AuthEvent):
    domain: str = BE_DOMAIN
    version: int = 1
    name: str = 'UserRegistered'
    body: UserRegisteredData


class UserCreated(AuthEvent):
    domain: str = CUD_DOMAIN + '.created'
    name: str = 'UserCreated'
    version: int = 1
    body: User

