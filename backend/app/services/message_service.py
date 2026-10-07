from sqlalchemy.orm import Session

from app.models.message import Message
from app.models.user import User
from app.repositories.message_repository import MessageRepository
from app.repositories.user_repository import UserRepository
from app.schemas.message import SendDirectMessageRequest
from app.strategies.message_strategy_factory import MessageStrategyFactory


class MessageService:

    def __init__(self, db: Session):
        self.message_repository = MessageRepository(db)
        self.user_repository = UserRepository(db)

    def send_direct_message(
        self,
        sender: User,
        request: SendDirectMessageRequest
    ) -> Message:

        strategy = MessageStrategyFactory.create(
            message_repository=self.message_repository,
            user_repository=self.user_repository,
            receiver_id=request.receiver_id
        )

        return strategy.send(
            sender=sender,
            content=request.content,
            receiver_id=request.receiver_id,
            media_url=request.media_url
        )

    def get_direct_messages(
        self,
        current_user: User,
        other_user_id: int
    ) -> list[Message]:

        other_user = self.user_repository.get_by_id(
            other_user_id
        )

        if not other_user:
            from fastapi import HTTPException, status

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return self.message_repository.get_direct_messages(
            user_id=current_user.user_id,
            other_user_id=other_user_id
        )