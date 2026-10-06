from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.contact import (
    AddContactRequest,
    ContactUserResponse,
)
from app.services.contact_service import ContactService


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)


@router.post(
    "",
    response_model=ContactUserResponse,
    status_code=status.HTTP_201_CREATED
)
def add_contact(
    request: AddContactRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ContactService(db)

    contact = service.add_contact(
        current_user,
        request
    )

    user = service.user_repository.get_by_id(
        contact.contact_user_id
    )

    return ContactUserResponse(
        user_id=user.user_id,
        phone_number=user.phone_number,
        username=user.username,
        profile_picture=user.profile_picture,
        status=user.status,
        last_seen=user.last_seen
    )


@router.get(
    "",
    response_model=list[ContactUserResponse]
)
def get_contacts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ContactService(db)

    return service.get_contacts(current_user)


@router.delete(
    "/{contact_user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_contact(
    contact_user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ContactService(db)

    service.remove_contact(
        current_user,
        contact_user_id
    )


@router.get(
    "/search",
    response_model=list[ContactUserResponse]
)
def search_users(
    q: str = Query(min_length=1, max_length=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ContactService(db)

    return service.search_users(
        current_user,
        q
    )