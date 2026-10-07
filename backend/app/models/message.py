from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    sender_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
        index=True
    )

    receiver_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=True,
        index=True
    )

    group_id: Mapped[int | None] = mapped_column(
        #ForeignKey("groups.group_id"),
        nullable=True,
        index=True
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    media_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="SENT"
    )