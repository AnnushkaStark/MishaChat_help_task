from sqlalchemy.ext.asyncio import AsyncSession

from crud.message import message_crud
from models import Message
from schemas.message import MessageCreate, MessageCreateDB
from utilities.attachment_schema import get_create_schema

from . import attachment as attachmet_service


async def create(
    db: AsyncSession, create_data: MessageCreate, chat_id: int, author_id: int
) -> Message:
    try:
        create_schema = MessageCreateDB(
            **create_data, author_id=author_id, chat_id=chat_id
        )
        message = await message_crud.create(
            db=db, create_schema=create_schema, commit=False
        )
        attachments = await get_create_schema(create_data.attachments)
        attachments_at_db = await attachmet_service.create(
            db=db, list_crate_data=attachments, message_id=message.id
        )
        message.attachments = attachments_at_db
        await db.commit()
        return message
    except Exception as ex:
        await db.rollback()
        raise ex
