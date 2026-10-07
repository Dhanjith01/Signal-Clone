from collections import defaultdict

from fastapi import WebSocket


class WebSocketManager:
    # using dict[int, set[WebSocket]] instead of dict[int, WebSocket]
    # because the same user can have multiple connections
    def __init__(self):
        self._connections: dict[int, set[WebSocket]] = defaultdict(set)

    async def connect(
        self,
        user_id: int,
        websocket: WebSocket
    ) -> None:
        await websocket.accept()
        self._connections[user_id].add(websocket)

    def disconnect(
        self,
        user_id: int,
        websocket: WebSocket
    ) -> None:
        connections = self._connections.get(user_id)

        if not connections:
            return

        connections.discard(websocket)

        if not connections:
            del self._connections[user_id]

    def is_online(self, user_id: int) -> bool:
        return bool(self._connections.get(user_id))

    async def send_to_user(
        self,
        user_id: int,
        message: dict
    ) -> None:
        connections = self._connections.get(user_id, set())

        disconnected = []

        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception:
                disconnected.append(websocket)

        for websocket in disconnected:
            self.disconnect(user_id, websocket)