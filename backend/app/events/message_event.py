from dataclasses import dataclass

from app.events.event import Event
from app.models.message import Message


@dataclass
class MessageCreatedEvent(Event):

    message: Message

    @property
    def event_type(self) -> str:
        return "message.created"