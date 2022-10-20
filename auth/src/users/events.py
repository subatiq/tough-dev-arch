from uuid import UUID
from brokereg import Event, EventData
from brokereg.common import CUD_Type, cud_topic
from src.users.model import User
from src.users.model import UserRole


REGISTRATION_FLOW = "user-registration"

CUD_AGGREGATE = 'user'
USER_CREATED = cud_topic(CUD_AGGREGATE, CUD_Type.CREATED)
USER_UPDATED = cud_topic(CUD_AGGREGATE, CUD_Type.UPDATED)


class AuthEvent(Event):
    producer: str = "auth"


class UserRegisteredData(EventData):
    pub_id: UUID
    username: str
    email: str
    role: UserRole


class UserRegistered(AuthEvent):
    domain: str = REGISTRATION_FLOW
    version: int = 1
    name: str = 'UserRegistered'
    body: UserRegisteredData


class UserCreated(AuthEvent):
    domain: str = USER_CREATED
    name: str = 'UserCreated'
    version: int = 1
    body: User

