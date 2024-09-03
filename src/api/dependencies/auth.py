from datetime import timedelta

from fastapi import Depends, HTTPException, Security
from fastapi_jwt import (
    JwtAccessBearerCookie,
    JwtAuthorizationCredentials,
    JwtRefreshBearer,
)
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.user import crud_user
from databases.database import get_async_session
from models import User
from schemas.token import TokenPayload
from settings import (
    JWT_ACCESS_TOKEN_EXPIRES,
    JWT_REFRESH_TOKEN_EXPIRES,
    JWT_SECRET_KEY,
)

access_security = JwtAccessBearerCookie(
    secret_key=JWT_SECRET_KEY,
    auto_error=True,
    access_expires_delta=timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRES),
)
refresh_security = JwtRefreshBearer(
    secret_key=JWT_SECRET_KEY,
    refresh_expires_delta=timedelta(minutes=JWT_REFRESH_TOKEN_EXPIRES),
    auto_error=True,
)


async def get_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        token_user = TokenPayload(**credentials.subject)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return await crud_user.get_by_username(db=db, username=token_user.username)