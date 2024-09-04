from sqlalchemy.ext.asyncio import AsyncSession

from crud.chat import chat_crud
from models import Chat
from schemas.chat import ChatCreate, ChatCreateDB
from utilities.check_participants import check_chat_participants


async def create(
    db: AsyncSession, create_data: ChatCreate, user_id: int
) -> Chat:
    try:
        create_schema = ChatCreateDB(
            **create_data.model_dump(exclude_unset=True),
            owner_id=user_id,
        )
        chat = await chat_crud.create(
            db=db, create_schema=create_schema, commit=False
        )
        chat.participants = await check_chat_participants(
            db=db,
            participants=create_data.participants_ids,
            chat_owner_id=user_id,
        )
        await db.commit()
        return chat
    except Exception as ex:
        await db.rollback()
        raise ex
