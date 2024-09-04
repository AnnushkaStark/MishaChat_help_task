from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import user_crud
from models import User
from schemas.user import UserCreate, UserCreateDB
from utilities.security.password_hasher import get_password_hash


async def create(db: AsyncSession, create_data: UserCreate) -> User:
    create_data.password = get_password_hash(create_data.password)
    db_schema = create_data.model_dump()
    create_schema = UserCreateDB(**db_schema)
    user = await user_crud.create(db=db, create_schema=create_schema)
    return user
