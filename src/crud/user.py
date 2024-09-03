from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from crud.async_crud import BaseAsyncCRUD
from models import User
from schemas.user import UserBase, UserCreateDB


class UserCRUD(BaseAsyncCRUD[User, UserCreateDB, UserBase]):
    async def get_by_username(
        self, db: AsyncSession, username: str
    ) -> Optional[User]:
        statement = select(self.model).where(self.model.username == username)
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_by_email(
        self, db: AsyncSession, email: str
    ) -> Optional[User]:
        statement = select(self.model).where(self.model.email == email)
        result = await db.execute(statement)
        return result.scalars().first()


user_crud = UserCRUD(User)
