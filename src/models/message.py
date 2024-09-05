from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

from .m2m import DeletedForUser

if TYPE_CHECKING:
    from .attachment import Attachment
    from .chat import Chat
    from .user import User


class Message(Base):
    """
    Модель сообщения

        ## Attrs:
            - id : int - Идентификатор сообщения
            - text : str -  текст сообщения
            - type : str(заглушка) -  тип сообщения
            - create_at: datetime - дата и вемя создания сообщения
            - updated_at: datetime -  дата и время изменения сообщения
            - deleted_at: datetime -  дата и время удаления сообщения
            - delete_for_me: bool- удалено для автора сообщения
            - delete_for_all: bool - удалено для всех пользователей чата
            - author_id: int - FK User - автор сообщения
            - author: User - связь  пользователь автор сообщения
            - deletd_for_user : List[User] - список пользователей которые
                удалили данное сообщение для себя связь М2M
            - chat_id: int FK Chat - идентификатор чата в который отправлено
                сообщение
            - chat: Chat - связь чат в которрый отпралено сообщение
            - attachments: List[Attachment] - связь вложения
    """

    __tablename__ = "message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(Text, default="")
    type: Mapped[str] = mapped_column(
        String, default=""  # Заглушка чтобы не делать энамы
    )
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    delete_for_all: Mapped[bool] = mapped_column(Boolean, default=False)
    author_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
    )
    author: Mapped["User"] = relationship(
        "User",
        back_populates="sent_messages",
    )
    deleted_for_user: Mapped[List["User"]] = relationship(
        "User",
        back_populates="messages_deleted_for_me",
        secondary=DeletedForUser.__table__,
    )
    chat_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("chat.id", ondelete="CASCADE"),
    )
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
    attachments: Mapped[List["Attachment"]] = relationship(
        "Attachment", back_populates="message"
    )

    def __repr__(self):
        return f"{self.text}"
