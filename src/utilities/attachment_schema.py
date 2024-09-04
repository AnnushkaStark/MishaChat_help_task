from typing import List

from schemas.attachment import AttachmentCreate


async def get_create_schema(attachments: List[str]) -> List[AttachmentCreate]:
    attachments = [
        AttachmentCreate(name=attachment) for attachment in attachments
    ]
    return attachments
