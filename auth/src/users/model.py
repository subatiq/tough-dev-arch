from __future__ import annotations
import hashlib
from uuid import UUID, uuid4
from pydantic import BaseModel, SecretStr
from pydantic.fields import Field


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: str
    username: str

    def to_db(self, password: SecretStr) -> UserInDB:
        return UserInDB(**self.dict(), password_hash=hashlib.md5(password.get_secret_value().encode()).digest())


class UserInDB(User):
    password_hash: bytes

    def to_public(self) -> User:
        return User(**self.dict(exclude={"password_hash"}))


class Credentials(BaseModel):
    username: str
    password: SecretStr


