from typing import Literal, Optional
from uuid import UUID

from fastapi import Cookie, FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, SecretStr

from src.tokens.model import ClientToken, Token, TokenState
from src.tokens.repo import InMemoryTokensRepository
import src.users.services as users_services
from src.tokens.services import check_token, get_refreshed_token
from src.users.model import Credentials, User, UserInDB
from src.users.repo import InMemoryUserRepository


app = FastAPI()
tokens_repo = InMemoryTokensRepository()
users_repo = InMemoryUserRepository()


@app.get("/user/{user_id}", response_model=User)
def index(
    response: Response,
    user_id: UUID,
    access_token: Optional[str] = Cookie(None),
    refresh_token: Optional[str] = Cookie(None),
) -> User | RedirectResponse | HTTPException:
    client_token = ClientToken(
        access_token=(access_token or ""), 
        refresh_token=(refresh_token or "")
    )

    saved_token = tokens_repo.token(user_id)

    if saved_token is None:
        return RedirectResponse("/login")

    token_state = check_token(client_token, saved_token)

    if token_state == TokenState.INVALID:
        return RedirectResponse("/login")

    elif token_state == TokenState.OUTDATED:
        refreshed_token = get_refreshed_token(tokens_repo, user_id, client_token)
        if refreshed_token is None:
            return HTTPException(status_code=401, detail="Access denied")

        response.set_cookie(key="access_token", value=refreshed_token.access_token)
        response.set_cookie(key="refresh_token", value=refreshed_token.refresh_token)
    
    user = users_repo.user(user_id)
    if user:
        return user
    else:
        return HTTPException(status_code=401, detail="Access denied")


@app.get("/login")
def login_page():
    return Response(content="Login page placeholder", status_code=401)


@app.post("/login")
def login(response: Response, creds: Credentials) -> UUID | HTTPException:
    user = users_repo.user_by_name(creds.username)
    
    if not user:
        return HTTPException(status_code=404, detail=f"User {creds.username} does not exist")

    token = tokens_repo.token(user.id)
    if not token:
        token = Token()
        tokens_repo.assign_token(user.id, token)

    if not users_services.login(user, creds.password):
        return HTTPException(status_code=401, detail="Access denied")
    

    response.set_cookie(key="access_token", value=token.access_token)
    response.set_cookie(key="refresh_token", value=token.refresh_token)

    return user.id


class UserRegistration(BaseModel):
    username: str
    email: str
    password: SecretStr

@app.post("/register")
def register(registring_user: UserRegistration):
    user = User(**registring_user.dict(exclude={'password'}))
    users_services.register(users_repo, user, registring_user.password)
    return user.id


@app.get("/debug/users", response_model=list[User])
def all_users():
    return [user.to_public() for user in users_repo.users.values()]
