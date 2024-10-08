from typing import List, Optional

from sqlalchemy import insert, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from crud.async_crud import BaseAsyncCRUD
from models import Chat
from schemas.chat import ChatCreateDB, ChatUpdate


class ChatCRUD(BaseAsyncCRUD[Chat, ChatCreateDB, ChatUpdate]):
    async def get_by_id_and_user_id(
        self, db: AsyncSession, obj_id: int, user_id: int
    ) -> Optional[Chat]:
        """
        вывод чата с участниками просто по чат айди и юзер айди
        (на всякий случай)
        """
        statement = (
            select(self.model)
            .options(
                joinedload(self.model.participants),
                joinedload(self.model.owner),
            )
            .where(self.model.id == obj_id)
        )
        statement = statement.where(
            or_(
                self.model.owner_id == user_id,
                self.model.participants.any(id=user_id),
            )
        )
        result = await db.execute(statement)
        return result.scalars().unique().first()

    async def get_by_owner_id(
        self, db: AsyncSession, owner_id: int
    ) -> List[Chat]:
        """
        Просмотр всех чатов с участниками
        созданных определенным
        пользователем
        """
        statement = (
            select(self.model)
            .options(
                joinedload(self.model.participants),
                joinedload(self.model.owner),
            )
            .where(self.model.id == owner_id)
        )
        result = await db.execute(statement)
        return result.scalars().unique().all()

    async def get_by_participant_id(
        self, db: AsyncSession, participant_id: int
    ) -> List[Chat]:
        """
        Просмотр всех чатов где пользовательявляется участником
        """
        statement = (
            select(self.model)
            .options(
                joinedload(self.model.participants),
                joinedload(self.model.owner),
            )
            .where(self.model.participants.any(id=participant_id))
        )
        result = await db.execute(statement)
        return result.scalars().unique().all()

    async def create(
        self,
        db: AsyncSession,
        create_schema: ChatCreateDB,
        commit: bool = True,
    ) -> Chat:
        data = create_schema.model_dump(exclude_unset=True)
        stmt = (
            insert(self.model)
            .values(**data)
            .returning(self.model)
            .options(
                selectinload(self.model.participants),
            )
        )
        res = await db.execute(stmt)
        if commit:
            await db.commit()
        return res.scalars().first()


chat_crud = ChatCRUD(Chat)
