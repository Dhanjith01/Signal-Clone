from fastapi import HTTPException, status

from app.repositories.message_repository import MessageRepository
from app.repositories.user_repository import UserRepository
from app.strategies.direct_message_strategy import DirectMessageStrategy
from app.strategies.message_strategy import MessageStrategy


class MessageStrategyFactory:

    @staticmethod
    def create(
        message_repository: MessageRepository,
        user_repository: UserRepository,
        receiver_id: int | None = None,
        group_id: int | None = None
    ) -> MessageStrategy:

        if receiver_id is not None and group_id is None:
            return DirectMessageStrategy(
                message_repository,
                user_repository
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid message destination"
        )