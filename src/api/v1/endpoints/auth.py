from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import refresh_security
from api.dependencies.database import get_async_db
from crud.user import user_crud
from models.user import User
from schemas.token import TokenAccessRefresh
from schemas.user import UserCreate, UserLogin
from services import user as service_user
from utilities.security.password_hasher import verify_password
from utilities.security.seciruty import TokenSubject, create_tokens

router = APIRouter()


@router.post(
    "/",
    summary="Create new user",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(get_async_db)
) -> User:
    existing_username = await user_crud.get_by_username(
        db, username=user.username
    )
    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username alredy exsist!",
        )
    existing_email = await user_crud.get_by_email(db, email=user.email)
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="E-mail alredy exsist!",
        )
    return await service_user.create(db=db, create_data=user)


@router.post("/login/", response_model=TokenAccessRefresh)
async def login(
    login_data: UserLogin, db: AsyncSession = Depends(get_async_db)
):
    if found_user := await user_crud.get_by_username(
        db, username=login_data.username
    ):
        if found_user:
            if verify_password(
                plain_password=login_data.password,
                hashed_password=found_user.password,
            ):
                subject = TokenSubject(
                    username=str(found_user.username),
                    password=found_user.password,
                )
                return await create_tokens(subject)
            raise HTTPException(
                status_code=401, detail="User password is wrong"
            )
        raise HTTPException(
            status_code=404,
            detail=f"User {login_data.username} has been deleted please contact support",  # noqa: E501
        )
    raise HTTPException(
        status_code=404, detail=f"User {login_data.username} not found."
    )


@router.post("/refresh/", response_model=TokenAccessRefresh)
async def refresh(
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
):
    return await create_tokens(credentials.subject)
