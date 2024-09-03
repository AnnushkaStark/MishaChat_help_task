from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

from .m2m import ChatUsers

if TYPE_CHECKING:
    from .message import Message
    from .user import User


class Chat(Base):
    """
    Модель чата

    ## Attrs
        - id: int -  идентификатор чата
        - title: str - название чата
        - created_at: datetime - дата и время создания чата
        - updated_at: datetime - дата и время обновления чата
        - privat_status: bool - статус приватный или нет
        - owner_id: int FK User - идентификатор пользователя
            создателя чата
        - owner: User - связь пользователь создатель чата
        - participants: List[User] - связь m2m - пользователи
            учатсники чата
        - messages: List[Messages] - сооьщения отправленные в чат
    """

    __tablename__ = "chat"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    privat_status: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
    )
    owner: Mapped["User"] = relationship("User", back_populates="chats_owner")
    participants: Mapped["User"] = relationship(
        "User",
        back_populates="chats_participant",
        secondary=ChatUsers.__table__,
    )
    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="chat"
    )

    def __repr__(self):
        return f"{self.title}"
