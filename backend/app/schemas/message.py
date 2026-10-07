from datetime import datetime

from pydantic import BaseModel, Field


class SendDirectMessageRequest(BaseModel):
    receiver_id: int
    content: str = Field(min_length=1, max_length=5000)
    media_url: str | None = None


class UpdateMessageStatusRequest(BaseModel):
    status: str


class MessageResponse(BaseModel):
    message_id: int
    sender_id: int
    receiver_id: int | None
    group_id: int | None
    content: str
    media_url: str | None
    timestamp: datetime
    status: str