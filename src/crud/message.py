from typing import List

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from crud.async_crud import BaseAsyncCRUD
from models import DeletedForUser, Message
from schemas.message import MessageCreateDB, MessageUpdate


class MessageCRUD(BaseAsyncCRUD[Message, MessageCreateDB, MessageUpdate]):
    async def get_by_chat_id(
        self, db: AsyncSession, chat_id: int, user_id: int
    ) -> List[Message]:
        statement = (
            select(self.model)
            .options(
                joinedload(self.model.author),
                joinedload(self.model.attachments),
                joinedload(self.model.deleted_for_user).joinedload(
                    DeletedForUser.user_id
                ),
            )
            .where(
                self.model.chat_id == chat_id,
                user_id != DeletedForUser.user_id,
            )
        )
        result = await db.execute(statement)
        return result.scalars().all()

    async def get_by_chat_id_and_user_id(
        self, db: AsyncSession, chat_id: int, user_id: int
    ) -> List[Message]:
        """
        Сообщения отправленные в опрделенный чат
        определенным пользователем,
        кроме тех которые он удалил для себя
        (вместо твоей таблички с отправленными))
        """
        statement = (
            select(self.model)
            .options(
                joinedload(self.model.author),
                joinedload(self.model.attachments),
                joinedload(self.model.deleted_for_user).joinedload(
                    DeletedForUser.user_id
                ),
            )
            .where(
                self.model.chat_id == chat_id,
                user_id != DeletedForUser.user_id,
                self.model.author_id == user_id,
            )
        )
        result = await db.execute(statement)
        return result.scalars().all()

    async def create(
        self,
        db: AsyncSession,
        create_schema: MessageCreateDB,
        commit: bool = True,
    ) -> Message:
        data = create_schema.model_dump(exclude_unset=True)
        stmt = (
            insert(self.model)
            .values(**data)
            .returning(self.model)
            .options(
                selectinload(self.model.attachments),
            )
        )
        res = await db.execute(stmt)
        if commit:
            await db.commit()
        return res.scalars().first()


message_crud = MessageCRUD(Message)
