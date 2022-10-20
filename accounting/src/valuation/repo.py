
from abc import ABC, abstractmethod
from uuid import UUID

from src.valuation.model import Valuation
from src.valuation.model import ValuationInDB


class ValuationsRepository(ABC):
    @abstractmethod
    def get(self, task_id: UUID):
        pass

    @abstractmethod
    def save(self, valuation: Valuation):
        pass
		

class InMemoryValuationRepository(ValuationsRepository):
    def __init__(self) -> None:
        self.valuations: dict[UUID, ValuationInDB] = {}


    def get(self, task_id: UUID) -> Valuation | None:
        for valuation in self.valuations.values():
            if valuation.task_id == task_id:
                return valuation

    def save(self, valuation: Valuation):
        db_val = ValuationInDB(**valuation.dict())
        self.valuations[db_val.id] = db_val
