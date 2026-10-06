from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(
            User.user_id == user_id
        )

        return self.db.scalar(statement)

    def get_by_phone_number(
        self,
        phone_number: str
    ) -> User | None:

        statement = select(User).where(
            User.phone_number == phone_number
        )

        return self.db.scalar(statement)

    def get_by_username(
        self,
        username: str
    ) -> User | None:

        statement = select(User).where(
            User.username == username
        )

        return self.db.scalar(statement)

    def create(
        self,
        phone_number: str,
        username: str
    ) -> User:

        user = User(
            phone_number=phone_number,
            username=username
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user