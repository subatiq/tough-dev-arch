from uuid import UUID
from brokereg import Event
from brokereg.common import CUD_Type, cud_topic
from pydantic import BaseModel
from src.users.models import User
from src.users.models import UserRole

REGISTRATION_FLOW = "user-registration"

CUD_AGGREGATE = 'user'
USER_CREATED = cud_topic(CUD_AGGREGATE, CUD_Type.CREATED)
USER_UPDATED = cud_topic(CUD_AGGREGATE, CUD_Type.UPDATED)


class UserRegisteredData(BaseModel):
    pub_id: UUID
    username: str
    email: str
    role: UserRole


class UserRegistered(BaseModel):
    domain: str = REGISTRATION_FLOW
    version: int = 1
    name: str = 'UserRegistered'
    body: UserRegisteredData


class UserCreated(Event):
    domain: str = USER_CREATED
    name: str = 'UserCreated'
    version: int = 1
    body: User
    

class UserUpdated(Event):
    domain: str = USER_UPDATED
    name: str = 'UserUpdated'
    version: int = 1
    body: User
