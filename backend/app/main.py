from fastapi import FastAPI, WebSocket

from app.core.config import settings
from app.database.database import Base, engine
from app.events.event import EventPublisher
from app.routers import auth_router, contacts_router, messages_router
from app.websocket.handler import handle_message_created, websocket_handler
from app.websocket.manager import WebSocketManager


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)


websocket_manager = WebSocketManager()
event_publisher = EventPublisher()


async def on_message_created(event):
    await handle_message_created(
        event,
        websocket_manager
    )


event_publisher.subscribe(
    "message.created",
    on_message_created
)

app.include_router(auth_router)
app.include_router(contacts_router)
app.include_router(messages_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_handler(
        websocket=websocket,
        manager=websocket_manager,
        event_publisher=event_publisher
    )