from typing import Optional

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from crud.async_crud import BaseAsyncCRUD
from models import DeletedForUser


class DeletForUserCRUD(BaseAsyncCRUD[DeletedForUser, BaseModel, BaseModel]):
    async def get_by_user_id_and_message_id(
        self, db: AsyncSession, user_id: int, message_id: int
    ) -> Optional[DeletedForUser]:
        statement = select(self.model).where(
            self.model.user_id == user_id, self.model.message_id == message_id
        )
        result = await db.execute(statement)
        return result.scalars().first()

    async def create_by_message_id_and_user_id(
        self, db: AsyncSession, user_id: int, message_id: int
    ) -> DeletedForUser:
        deleted_for_user_message = self.model(
            user_id=user_id, message_id=message_id
        )
        db.add(deleted_for_user_message)
        await db.commit()
        await db.refresh(deleted_for_user_message)
        return deleted_for_user_message


delete_for_user_crud = DeletForUserCRUD(DeletedForUser)
