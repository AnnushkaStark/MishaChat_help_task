from datetime import timedelta
from typing import TypedDict

from api.dependencies.auth import access_security, refresh_security
from schemas.token import TokenAccessRefresh
from settings import JWT_REFRESH_TOKEN_EXPIRES


class TokenSubject(TypedDict):
    username: str
    password: str


async def create_tokens(subject: TokenSubject) -> TokenAccessRefresh:
    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(
        subject=subject,
        expires_delta=timedelta(minutes=JWT_REFRESH_TOKEN_EXPIRES),
    )
    return TokenAccessRefresh(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


ACCESS_TOKEN_COOKIE_KEY = "access_token_cookie"
REFRESH_TOKEN_COOKIE_KEY = "refresh_token_cookie"