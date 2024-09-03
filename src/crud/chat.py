from typing import Optional

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from crud.async_crud import BaseAsyncCRUD
from models import Chat
from schemas.chat import ChatCreateDB, ChatUpdate


class ChatCRUD(BaseAsyncCRUD[Chat, ChatCreateDB, ChatUpdate]):
    async def get_by_id_with_participants(
        self, db: AsyncSession, obj_id: int
    ) -> Optional[Chat]:
        """
        вывод чата с участниками
        (на всякий случай)
        """
        statement = (
            select(self.model)
            .options(joinedload(self.model.participants))
            .where(self.model.id == obj_id)
        )
        result = await db.execute(statement)
        return result.scalars().first()

    async def get_by_owner_id(
        self, db: AsyncSession, owner_id: int
    ) -> Optional[Chat]:
        """
        Просмотр всех чатов с участниками
        созданных определенным
        пользователем
        """
        statement = (
            select(self.model)
            .options(joinedload(self.model.participants))
            .where(self.model.id == owner_id)
        )
        result = await db.execute(statement)
        return result.scalars().first()

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
