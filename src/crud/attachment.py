from typing import List

from sqlalchemy import insert
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
        result_data = [s.model_dump() for s in list_data]
        stmt = insert(self.model).values(result_data).returning(self.model)
        result = await db.execute(stmt)
        objs = result.scalars().all()
        await db.commit()
        return objs


attachment_crud = AttachmentCRUD(Attachment)
