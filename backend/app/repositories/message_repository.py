from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.message import Message


class MessageRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        sender_id: int,
        receiver_id: int,
        content: str,
        media_url: str | None = None
    ) -> Message:

        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            media_url=media_url,
            status="SENT"
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_by_id(
        self,
        message_id: int
    ) -> Message | None:

        statement = select(Message).where(
            Message.message_id == message_id
        )

        return self.db.scalar(statement)

    def get_direct_messages(
        self,
        user_id: int,
        other_user_id: int
    ) -> list[Message]:

        statement = (
            select(Message)
            .where(
                Message.group_id.is_(None),
                or_(
                    (
                        Message.sender_id == user_id
                    ) & (
                        Message.receiver_id == other_user_id
                    ),
                    (
                        Message.sender_id == other_user_id
                    ) & (
                        Message.receiver_id == user_id
                    )
                )
            )
            .order_by(Message.timestamp.asc())
        )

        return list(self.db.scalars(statement).all())

    def update_status(
        self,
        message: Message,
        status: str
    ) -> Message:

        message.status = status

        self.db.commit()
        self.db.refresh(message)

        return message