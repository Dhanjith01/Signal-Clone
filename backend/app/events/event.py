from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Awaitable, Callable


EventHandler = Callable[["Event"], Awaitable[None]]


class Event(ABC):

    @property
    @abstractmethod
    def event_type(self) -> str:
        pass


class EventPublisher:

    def __init__(self):
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(
        self,
        event_type: str,
        handler: EventHandler
    ) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, event: Event) -> None:
        handlers = self._handlers.get(event.event_type, [])

        for handler in handlers:
            await handler(event)