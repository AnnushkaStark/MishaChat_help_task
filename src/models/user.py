from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

from .m2m import ChatUsers

if TYPE_CHECKING:
    from .chat import Chat
    from .message import Message


class User(Base):
    """
    Модель пользователя

    ## Attrs:
       - id: int - идентификатор пользователя
       - username: str - юзернейм пользователя
       - updated_at: datetime - дата и время обновления данных
       - status: str - сетевой статус пользователя (заглушка)
       - online_at: datetime - когда последний  раз был онлайн
       - sent_messages: List[Message] - аналог табличке Forwarded
            (сообщения отправленные пользователем)
       - chats_owner: List[Chat] - чаты которые создал пользователь
       - chat_participant: List[Chat] - чаты в которых учавствует пользователь

    """

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    status: Mapped[str] = mapped_column(
        String, default=""
    )  # Просто заглушка для статуса
    online_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    sent_messages: Mapped[
        List["Message"]
    ] = relationship(  # отправленные сообщения
        "Message", back_populates="author"
    )
    chats_owner: Mapped[List["Chat"]] = relationship(
        "Chat", back_populates="owner"
    )
    chat_participant: Mapped[List["Chat"]] = relationship(
        "Chat",
        secondary=ChatUsers.__table__,
        back_populates="participants",
    )

    def __repr__(self):
        return f"{self.username}"
