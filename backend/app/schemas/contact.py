from datetime import datetime

from pydantic import BaseModel


class AddContactRequest(BaseModel):
    contact_user_id: int


class ContactResponse(BaseModel):
    contact_id: int
    user_id: int
    contact_user_id: int
    created_at: datetime


class ContactUserResponse(BaseModel):
    user_id: int
    phone_number: str
    username: str
    profile_picture: str | None
    status: str | None
    last_seen: datetime | None