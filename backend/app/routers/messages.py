from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.message import (
    MessageResponse,
    SendDirectMessageRequest,
    UpdateMessageStatusRequest
)
from app.services.message_service import MessageService


router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)


@router.post(
    "/direct",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED
)
def send_direct_message(
    request: SendDirectMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = MessageService(db)

    return service.send_direct_message(
        current_user,
        request
    )


@router.get(
    "/direct/{user_id}",
    response_model=list[MessageResponse]
)
def get_direct_messages(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = MessageService(db)

    return service.get_direct_messages(
        current_user,
        user_id
    )
    
@router.patch(
    "/{message_id}/status",
    response_model=MessageResponse
)
def update_message_status(
    message_id: int,
    request: UpdateMessageStatusRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = MessageService(db)

    return service.update_message_status(
        current_user=current_user,
        message_id=message_id,
        new_status=request.status
    )