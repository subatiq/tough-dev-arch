from typing import Literal
from uuid import UUID

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, SecretStr

from src.tokens.model import ClientToken, Token, TokenState
from src.tokens.repo import InMemoryTokensRepository
import src.users.services as users_services
from src.tokens.services import check_token, get_refreshed_token
from src.users.model import Credentials, User, UserRole
from src.users.repo import InMemoryUserRepository


app = FastAPI()
tokens_repo = InMemoryTokensRepository()
users_repo = InMemoryUserRepository()



@app.get("/login")
def login_page():
    return Response(content="Login page placeholder", status_code=401)


@app.post("/login")
def login(response: Response, creds: Credentials) -> UUID:
    user = users_repo.user_by_name(creds.username)
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User {creds.username} does not exist")

    token = tokens_repo.token(user.id)
    if not token:
        token = Token()
        tokens_repo.assign_token(user.id, token)

    if not users_services.login(user, creds.password):
        raise HTTPException(status_code=401, detail="Access denied")
    

    response.set_cookie(key="access_token", value=token.access_token)
    response.set_cookie(key="refresh_token", value=token.refresh_token)

    return user.id


@app.post("/authz")
def authorize(ctoken: ClientToken):
    user_id = tokens_repo.user_id(ctoken.access_token)
    if not user_id:
        raise HTTPException(status_code=404, detail=f"User does not exist")

    user = users_repo.user(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User does not exist")

    token = tokens_repo.token(user.id)
    if not token:
        raise HTTPException(status_code=404, detail="No auth info for user")

    print(tokens_repo.tokens)
    if not (tokens_repo.token(user_id) or Token()).access_token == ctoken.access_token:
        raise HTTPException(status_code=401, detail="Access denied")
    
    return True


class UserRegistration(BaseModel):
    username: str
    email: str
    role: UserRole
    password: SecretStr

@app.post("/register")
def register(registring_user: UserRegistration):
    user = User(**registring_user.dict(exclude={'password'}))
    users_services.register(users_repo, user, registring_user.password)
    return user.id


@app.get("/debug/users", response_model=list[User])
def all_users():
    return [user.to_public() for user in users_repo.users.values()]

