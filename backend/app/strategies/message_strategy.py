from abc import ABC, abstractmethod

from app.models.message import Message
from app.models.user import User


class MessageStrategy(ABC):

    @abstractmethod
    def send(
        self,
        sender: User,
        content: str,
        receiver_id: int | None = None,
        group_id: int | None = None,
        media_url: str | None = None
    ) -> Message:
        pass