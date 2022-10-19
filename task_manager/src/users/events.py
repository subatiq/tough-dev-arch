from brokereg import Event
from src.users.model import User

CUD_DOMAIN = 'user-streaming'


class UserCreated(Event):
    domain: str = CUD_DOMAIN + '.created'
    name: str = 'UserCreated'
    version: int = 1
    body: User

