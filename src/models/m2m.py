from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from databases.database import Base


class ChatUsers(Base):
    """
    Модель участников события m2m

    ## Attrs
        - chat_id : int - идентификатор чата
        - user_id : int - идентификатор пользователя (участника)
    """

    __tablename__ = "chat_users"
    __table_args__ = (
        UniqueConstraint("chat_id", "user_id", name="uix_chat_user"),
    )

    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chat.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    )


class DeletedForUser(Base):
    """
    Модель удаленных сообщений для определеннго пользователя

    ## Attrs:
        - message_id: int - идентификатор сообщения
        -  user_id - идентификатор пользователя
            для котрого оно удалено
    """

    __tablename__ = "deleted_for_user"
    __table_args__ = (
        UniqueConstraint("message_id", "user_id", name="uix_deletd_message"),
    )
    message_id: Mapped[int] = mapped_column(
        ForeignKey("message.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
