from uuid import UUID
from brokereg import Event, EventData
from brokereg.common import CUD_Type, cud_topic

from src.accounts.models import Account

PAYMENT_FLOW = "user-payments"

CUD_AGGREGATE = 'account'
ACCOUNT_UPDATED = cud_topic(CUD_AGGREGATE, CUD_Type.UPDATED)
ACCOUNT_CREATED = cud_topic(CUD_AGGREGATE, CUD_Type.CREATED)


class AccountingEvent(Event):
    producer: str = "accounting"


class UserGotPayedData(EventData):
    user_id: UUID


class UserGotPayed(AccountingEvent):
    domain: str = PAYMENT_FLOW
    name = "UserGotPayed"
    version: int = 1
    body: UserGotPayedData


class BillingCycleCompletedData(EventData):
    user_id: UUID


class BillingCycleCompleted(AccountingEvent):
    domain: str = PAYMENT_FLOW
    name = "BillingCycleCompleted"
    version: int = 1
    body: BillingCycleCompletedData 


class AccountCreated(AccountingEvent):
    domain: str =  ACCOUNT_CREATED
    name: str = "AccountCreated"
    version: int = 1
    body: Account


class AccountUpdated(AccountingEvent):
    domain: str =  ACCOUNT_UPDATED
    name: str = "AccountUpdated"
    version: int = 1
    body: Account

