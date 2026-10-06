from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_otp
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    OTPVerifyRequest,
    RegisterRequest,
    RegisterResponse,
)


class AuthService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def register(self, request: RegisterRequest) -> RegisterResponse:
        existing_user = self.user_repository.get_by_phone_number(
            request.phone_number
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Phone number is already registered"
            )

        existing_user = self.user_repository.get_by_username(
            request.username
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username is already taken"
            )

        user = self.user_repository.create(
            phone_number=request.phone_number,
            username=request.username
        )

        return RegisterResponse(
            user_id=user.user_id,
            phone_number=user.phone_number,
            username=user.username,
            message="User registered successfully"
        )

    def request_login_otp(
        self,
        request: LoginRequest
    ) -> dict:

        user = self.user_repository.get_by_phone_number(
            request.phone_number
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return {
            "message": "OTP sent successfully",
            "otp": "123456"
        }

    def verify_login_otp(
        self,
        request: OTPVerifyRequest
    ) -> LoginResponse:

        user = self.user_repository.get_by_phone_number(
            request.phone_number
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not verify_otp(request.otp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid OTP"
            )

        access_token = create_access_token(user.user_id)

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.user_id,
            username=user.username
        )