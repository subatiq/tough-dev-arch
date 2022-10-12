from abc import ABC, abstractmethod
from uuid import UUID

from src.tokens.model import Token


class TokensRepository(ABC):
    @abstractmethod
    def assign_token(self, user_id: UUID, token: Token):
        pass

    @abstractmethod
    def token(self, user_id: UUID) -> Token | None:
        pass


class InMemoryTokensRepository(TokensRepository):
    def __init__(self) -> None:
        self.tokens = {}

    def assign_token(self, user_id: UUID, token: Token):
        self.tokens[user_id] = token

    def token(self, user_id: UUID) -> Token | None:
        return self.tokens.get(user_id)

