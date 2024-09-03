from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

from .m2m import ChatUsers, DeletedForUser

if TYPE_CHECKING:
    from .chat import Chat
    from .message import Message


class User(Base):
    """
    Модель пользователя

    ## Attrs:
       - id: int - идентификатор пользователя
       - username: str - юзернейм пользователя
       - email: str - электронная почта пользователя ( временное поле)
       - password: str - парроль пользователя - временное поле
       - updated_at: datetime - дата и время обновления данных
       - status: str - сетевой статус пользователя (заглушка)
       - online_at: datetime - когда последний  раз был онлайн
       - sent_messages: List[Message] - аналог табличке Forwarded
            (сообщения отправленные пользователем)
       - messages_deleted_for_me: List[Message] - сообщения чата которые
          пользователь удалил для себя связь М2M
       - chats_owner: List[Chat] - чаты которые создал пользователь
       - chat_participant: List[Chat] - чаты в которых учавствует пользователь

    """

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str]
    password: Mapped[str]
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
        "Message",
        back_populates="author",
    )
    messages_deleted_for_me: Mapped[List["Message"]] = relationship(
        "Message",
        back_populates="deleted_for_user",
        secondary=DeletedForUser.__table__,
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
