from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from crud.async_crud import BaseAsyncCRUD
from models import Attachment
from schemas.attachment import AttachmentCreateDB, AttachmentUpdate


class AttachmentCRUD(
    BaseAsyncCRUD[Attachment, AttachmentCreateDB, AttachmentUpdate]
):
    async def bulk_create(
        self, db: AsyncSession, list_data: List[AttachmentCreateDB]
    ) -> List[Attachment]:
        result = await self.create(Attachment(**data) for data in list_data)
        await db.commit()
        return result


attachment_crud = AttachmentCRUD(Attachment)
