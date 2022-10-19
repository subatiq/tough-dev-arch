from datetime import datetime
from uuid import UUID
from src.tokens.model import ClientToken, Token, TokenState
from src.tokens.repo import TokensRepository


def check_token(client_token: ClientToken, token: Token) -> TokenState:
    if token.expires_at < datetime.utcnow():
        return TokenState.OUTDATED

    if token.access_token == client_token.access_token:
        return TokenState.OK

    return TokenState.INVALID


def update_token(repo: TokensRepository, user_id: UUID) -> Token:
    updated_token = Token()
    repo.assign_token(user_id, updated_token)
    return updated_token


def get_refreshed_token(repo: TokensRepository, user_id: UUID, token: ClientToken) -> Token | None:
    saved_token = repo.token(user_id)
    if saved_token is None:
        return 

    updated_token = update_token(repo, user_id)

    # Return updated token in case everything is good
    # Otherwise DB is updated with random token which invalidates
    # all previous access and refresh tokens (RT rotation)
    if token.refresh_token == saved_token.refresh_token:
        return updated_token

