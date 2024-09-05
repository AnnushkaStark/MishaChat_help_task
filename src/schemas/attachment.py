from typing import Optional

from pydantic import BaseModel, Field


class AttachmentBase(BaseModel):
    name: str = Field(max_length=100, min_length=3)
    path: str = Field(default="/quniq/attachments/")
    type: str = Field(default="pdf")

    class Config:
        from_attributes = True


class AttachmentCreate(AttachmentBase):
    ...


class AttachmentCreateDB(AttachmentCreate):
    message_id: int

    class Config:
        from_attributes = True


class AttachmentUpdate(AttachmentBase):
    name: Optional[str] = Field(max_length=100, min_length=3)
    path: Optional[str] = Field(default="/quniq/attachments/")
    type: Optional[str] = Field(default="pdf")

    class Config:
        from_attributes = True


class AttachmentResponse(AttachmentBase):
    chat_id: int
