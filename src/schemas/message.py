from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .attachment import AttachmentResponse
from .user import UserResponse


class MessageBase(BaseModel):
    text: Optional[str] = Field(default="")

    class Config:
        from_attributes = True


class MessageCreate(MessageBase):
    attachments: List[str] = []

    class Config:
        from_attributes = True


class MessageCreateDB(MessageBase):
    author_id: int
    chat_id: int

    class Config:
        from_attributes = True


class MessageUpdate(MessageBase):
    attachments: List[str] = []

    class Config:
        from_attributes = True


class MessageResponse(MessageBase):
    id: int
    author_id: int
    chat_id: int
    author: UserResponse
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    attachments: List[AttachmentResponse] = []
