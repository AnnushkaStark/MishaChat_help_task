from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from crud.attachment import attachment_crud
from models import Attachment
from schemas.attachment import AttachmentCreate, AttachmentCreateDB


async def create(
    db: AsyncSession, list_crate_data: List[AttachmentCreate], message_id: int
) -> Attachment:
    list_create_schema = [
        AttachmentCreateDB(**create_data.model_dump(), message_id=message_id)
        for create_data in list_crate_data
    ]
    attachments = await attachment_crud.bulk_create(
        db=db, list_data=list_create_schema
    )
    return attachments
