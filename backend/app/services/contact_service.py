from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.contact_repository import ContactRepository
from app.repositories.user_repository import UserRepository
from app.schemas.contact import (
    AddContactRequest,
    ContactUserResponse,
)


class ContactService:

    def __init__(self, db: Session):
        self.contact_repository = ContactRepository(db)
        self.user_repository = UserRepository(db)

    def add_contact(
        self,
        current_user: User,
        request: AddContactRequest
    ):
        if current_user.user_id == request.contact_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot add yourself as a contact"
            )

        contact_user = self.user_repository.get_by_id(
            request.contact_user_id
        )

        if not contact_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        existing_contact = self.contact_repository.get_contact(
            current_user.user_id,
            request.contact_user_id
        )

        if existing_contact:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already a contact"
            )

        return self.contact_repository.create(
            user_id=current_user.user_id,
            contact_user_id=request.contact_user_id
        )

    def get_contacts(
        self,
        current_user: User
    ) -> list[ContactUserResponse]:

        contacts = self.contact_repository.get_contacts(
            current_user.user_id
        )

        result = []

        for contact in contacts:
            user = self.user_repository.get_by_id(
                contact.contact_user_id
            )

            if user:
                result.append(
                    ContactUserResponse(
                        user_id=user.user_id,
                        phone_number=user.phone_number,
                        username=user.username,
                        profile_picture=user.profile_picture,
                        status=user.status,
                        last_seen=user.last_seen
                    )
                )

        return result

    def remove_contact(
        self,
        current_user: User,
        contact_user_id: int
    ) -> None:

        contact = self.contact_repository.get_contact(
            current_user.user_id,
            contact_user_id
        )

        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found"
            )

        self.contact_repository.delete(contact)

    def search_users(
        self,
        current_user: User,
        query: str
    ) -> list[ContactUserResponse]:

        users = self.user_repository.search(query)

        return [
            ContactUserResponse(
                user_id=user.user_id,
                phone_number=user.phone_number,
                username=user.username,
                profile_picture=user.profile_picture,
                status=user.status,
                last_seen=user.last_seen
            )
            for user in users
            if user.user_id != current_user.user_id
        ]