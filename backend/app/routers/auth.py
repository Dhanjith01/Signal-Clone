from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    OTPVerifyRequest,
    RegisterRequest,
    RegisterResponse,
)
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=201
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)

    return auth_service.register(request)


@router.post("/login/request")
def request_login_otp(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)

    return auth_service.request_login_otp(request)


@router.post(
    "/login/verify",
    response_model=LoginResponse
)
def verify_login_otp(
    request: OTPVerifyRequest,
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)

    return auth_service.verify_login_otp(request)