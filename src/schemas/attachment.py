from typing import  Optional

from pydantic import BaseModel, Field


class AttachmentBase(BaseModel):
    name: str =Field(max_length=100, min_length=3)
    path: str = Field(default="")
    type: str = Field(default="")

    class Config:
        from_attributes = True


class AttachmentCreate(AttachmentBase):
    ... 


class AttachmentUpdate(AttachmentCreate):
    message_id: int


class AttachmentUpdate(AttachmentBase):
    name: Optional[str] =Field(max_length=100, min_length=3)
    path: Optional[str] = Field(default="")
    type: Optional[str] = Field(default="")

    class Config:
        from_attributes = True


class AttachmentResponse(AttachmentBase):
    chat_id : int