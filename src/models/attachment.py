from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.database import Base

if TYPE_CHECKING:
    from .message import Message


class Attachment(Base):
    """
    Модель вложения
     ## Attrs:
        - id: int - идентификатор вложения
        - name: str - название файла вложения (заглушка)
        - path: str - путь к файлу - вложения (заглушка)
        - type: str - тип файла вложения (заглушка)
        - message_id: int FK mesage - идентификатор сообщения
            в которое добалено вложение
        - message: Message - связь сообщение в которое добавлено
            вложение

    """

    __tablename__ = "attachment"
    __table_args__ = (UniqueConstraint("name", "path", name="uix_file_path"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String, default=""
    )  # Заглушка название файла
    path: Mapped[str] = mapped_column(
        String, default=""
    )  # Заглушка путь к файлу
    type: Mapped[str] = mapped_column(String, default="")  # Заглушка тип файла
    message_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
    )
    message: Mapped["Message"] = relationship(
        "Message", back_populates="attachments"
    )

    def __repr__(self):
        return f"{self.name} {self.path}"
