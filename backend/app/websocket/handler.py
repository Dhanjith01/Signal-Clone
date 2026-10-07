from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from app.core.security import decode_access_token
from app.database.database import SessionLocal
from app.events.event import EventPublisher
from app.events.message_event import MessageCreatedEvent
from app.repositories.user_repository import UserRepository
from app.schemas.message import SendDirectMessageRequest
from app.services.message_service import MessageService
from app.websocket.manager import WebSocketManager


async def handle_message_created(
    event: MessageCreatedEvent,
    manager: WebSocketManager
) -> None:
    message = event.message

    payload = {
        "type": "message.new",
        "message": {
            "message_id": message.message_id,
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id,
            "group_id": message.group_id,
            "content": message.content,
            "media_url": message.media_url,
            "timestamp": message.timestamp.isoformat(),
            "status": message.status,
        }
    }

    await manager.send_to_user(
        message.sender_id,
        payload
    )

    if message.receiver_id is not None:
        await manager.send_to_user(
            message.receiver_id,
            payload
        )


async def websocket_handler(
    websocket: WebSocket,
    manager: WebSocketManager,
    event_publisher: EventPublisher
) -> None:

    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return

    try:
        user_id = decode_access_token(token)
    except ValueError:
        await websocket.close(code=1008)
        return

    db = SessionLocal()

    try:
        user_repository = UserRepository(db)
        user = user_repository.get_by_id(user_id)
    finally:
        db.close()

    if not user:
        await websocket.close(code=1008)
        return

    await manager.connect(user.user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("type") != "message.send":
                await websocket.send_json({
                    "type": "error",
                    "message": "Unsupported message type"
                })
                continue

            try:
                request = SendDirectMessageRequest.model_validate(data)
            except ValidationError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid message payload"
                })
                continue

            db = SessionLocal()

            try:
                user_repository = UserRepository(db)
                current_user = user_repository.get_by_id(user_id)

                if not current_user:
                    await websocket.send_json({
                        "type": "error",
                        "message": "User no longer exists"
                    })
                    continue

                message_service = MessageService(db)

                message = message_service.send_direct_message(
                    current_user,
                    request
                )

                event = MessageCreatedEvent(message)

            except Exception as exc:
                await websocket.send_json({
                    "type": "error",
                    "message": str(exc)
                })
                continue

            finally:
                db.close()

            await event_publisher.publish(event)

    except WebSocketDisconnect:
        pass

    finally:
        manager.disconnect(user_id, websocket)