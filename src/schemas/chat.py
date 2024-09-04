from typing import List, Optional

from pydantic import BaseModel, Field

from .user import UserResponse


class ChatBase(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    privat_status: Optional[bool] = Field(default=False)

    class Config:
        from_attributes = True


class ChatCreate(ChatBase):
    participants_ids: List[int] = []

    class Config:
        from_attributes = True


class ChatCreateDB(ChatBase):
    owner_id: int

    class Config:
        from_attributes = True


class ChatUpdate(ChatBase):
    title: Optional[str] = Field(min_length=3, max_length=50)
    privat_status: Optional[bool] = Field(default=False)
    participants_ids: List[int] = []


class ChatResponse(ChatBase):
    id: int
    title: str
    owner_id: int
    owner: UserResponse
    privat_status: bool = Field(default=False)
    participants: List[UserResponse]
