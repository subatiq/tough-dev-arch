
from uuid import UUID
from brokereg import Event, EventData
from brokereg.common import CUD_Type, cud_topic
from src.valuation.model import Valuation

CUD_AGGREGATE = 'valuation'
VALUATION_UPDATED = cud_topic(CUD_AGGREGATE, CUD_Type.UPDATED)
VALUATION_CREATED = cud_topic(CUD_AGGREGATE, CUD_Type.CREATED)


class ValuationEvent(Event):
    producer = "accounting"


class ValuationUpdated(ValuationEvent):
    domain: str =  VALUATION_UPDATED
    name: str = "ValuationUpdated"
    version: int = 1
    body: Valuation


class ValuationCreated(ValuationEvent):
    domain: str = VALUATION_CREATED
    name: str = "ValuationCreated"
    version: int = 1
    body: Valuation
