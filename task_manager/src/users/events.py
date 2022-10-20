from brokereg import Event
from src.users.model import User
from brokereg.common import cud_topic, CUD_Type
from src.task.events import CUD_AGGREGATE

CUD_AGGREGATE = 'user'
USER_CREATED = cud_topic(CUD_AGGREGATE, CUD_Type.CREATED)


class UserCreated(Event):
    domain: str = USER_CREATED
    name: str = 'UserCreated'
    version: int = 1
    body: User

