from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.contact import Contact


class ContactRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        contact_id: int
    ) -> Contact | None:

        statement = select(Contact).where(
            Contact.contact_id == contact_id
        )

        return self.db.scalar(statement)

    def get_contact(
        self,
        user_id: int,
        contact_user_id: int
    ) -> Contact | None:

        statement = select(Contact).where(
            Contact.user_id == user_id,
            Contact.contact_user_id == contact_user_id
        )

        return self.db.scalar(statement)

    def get_contacts(
        self,
        user_id: int
    ) -> list[Contact]:

        statement = (
            select(Contact)
            .where(Contact.user_id == user_id)
            .order_by(Contact.created_at.desc())
        )

        return list(self.db.scalars(statement).all())

    def create(
        self,
        user_id: int,
        contact_user_id: int
    ) -> Contact:

        contact = Contact(
            user_id=user_id,
            contact_user_id=contact_user_id
        )

        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)

        return contact

    def delete(
        self,
        contact: Contact
    ) -> None:

        self.db.delete(contact)
        self.db.commit()