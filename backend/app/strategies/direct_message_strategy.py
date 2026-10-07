from fastapi import HTTPException, status

from app.models.message import Message
from app.models.user import User
from app.repositories.message_repository import MessageRepository
from app.repositories.user_repository import UserRepository

from app.strategies.message_strategy import MessageStrategy


class DirectMessageStrategy(MessageStrategy):

    def __init__(
        self,
        message_repository: MessageRepository,
        user_repository: UserRepository
    ):
        self.message_repository = message_repository
        self.user_repository = user_repository

    def send(
        self,
        sender: User,
        content: str,
        receiver_id: int | None = None,
        group_id: int | None = None,
        media_url: str | None = None
    ) -> Message:

        if receiver_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Receiver is required for a direct message"
            )

        if group_id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Group ID is not allowed for a direct message"
            )

        if sender.user_id == receiver_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot send a message to yourself"
            )

        receiver = self.user_repository.get_by_id(receiver_id)

        if not receiver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receiver not found"
            )

        return self.message_repository.create(
            sender_id=sender.user_id,
            receiver_id=receiver_id,
            content=content,
            media_url=media_url
        )