from typing import List, Optional

from sqlalchemy import insert, not_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from crud.async_crud import BaseAsyncCRUD
from models import Message
from schemas.message import MessageCreateDB, MessageUpdate


class MessageCRUD(BaseAsyncCRUD[Message, MessageCreateDB, MessageUpdate]):
    async def get_by_id_and_user_id(
        self, db: AsyncSession, obj_id: int, user_id: int
    ) -> Optional[Message]:
        """
        Выбирает одно сообщение пользователя
        (если пользователь не удалил его для себя)
        """
        statement = (
            select(self.model)
            .options(
                joinedload(self.model.attachments),
                joinedload(self.model.deleted_for_user),
                joinedload(self.model.chat),
                joinedload(self.model.author),
            )
            .where(
                self.model.id == obj_id,
                not_(self.model.deleted_for_user.any(id=user_id)),
                self.model.delete_for_all.is_(False),
            )
        )

        result = await db.execute(statement)
        return result.scalars().unique().first()

    async def get_by_chat_id_and_user_id(
        self, db: AsyncSession, chat_id: int, user_id: int
    ) -> List[Message]:
        """
        Выбирает все сообщения чата (история чата) -
        кроме тех сообщений которые пользователь
        удалил для себя
        """
        statement = (
            select(self.model)
            .options(
                joinedload(self.model.author),
                joinedload(self.model.attachments),
                joinedload(self.model.deleted_for_user),
            )
            .where(
                self.model.chat_id == chat_id,
                not_(self.model.deleted_for_user.any(id=user_id)),
                self.model.delete_for_all.is_(False),
            )
        )
        result = await db.execute(statement)
        return result.scalars().unique().all()

    async def get_by_chat_id_and_author_id(
        self, db: AsyncSession, chat_id: int, author_id: int
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
                joinedload(self.model.deleted_for_user),
            )
            .where(
                self.model.chat_id == chat_id,
                self.model.author_id == author_id,
                not_(self.model.deleted_for_user.any(id=author_id)),
                self.model.delete_for_all.is_(False),
            )
        )
        result = await db.execute(statement)
        return result.scalars().unique().all()

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
                selectinload(self.model.author),
                selectinload(self.model.attachments),
                selectinload(self.model.chat),
                selectinload(self.model.deleted_for_user),
            )
        )
        res = await db.execute(stmt)
        if commit:
            await db.commit()
        return res.scalars().first()

    async def mark_deleted(
        self, db: AsyncSession, user_id: int, message_id: int
    ) -> Message:
        if found_message := await self.get_by_id_and_user_id(
            db=db, user_id=user_id, obj_id=message_id
        ):
            found_message.delete_for_all = True
            db.add(found_message)
            await db.commit()
            await db.refresh(found_message)
            return found_message


message_crud = MessageCRUD(Message)
