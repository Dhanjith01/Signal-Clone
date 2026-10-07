from sqlalchemy.orm import Session

from app.models.message import Message
from app.models.user import User
from app.repositories.message_repository import MessageRepository
from app.repositories.user_repository import UserRepository
from app.schemas.message import SendDirectMessageRequest
from app.strategies.message_strategy_factory import MessageStrategyFactory
from fastapi import HTTPException, status
from app.core.constants import MessageStatus

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
        
    def update_message_status(
        self,
        current_user: User,
        message_id: int,
        new_status: str
    ) -> Message:

        if new_status not in MessageStatus.VALID_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid message status"
            )
    
        message = self.message_repository.get_by_id(
            message_id
        )
    
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
    
        if message.receiver_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot update this message status"
            )
    
        status_order = {
            MessageStatus.SENT: 1,
            MessageStatus.DELIVERED: 2,
            MessageStatus.READ: 3,
        }
    
        current_status = status_order.get(message.status)
        requested_status = status_order.get(new_status)
    
        if requested_status < current_status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message status cannot move backwards"
            )
    
        return self.message_repository.update_status(
            message,
            new_status
        )