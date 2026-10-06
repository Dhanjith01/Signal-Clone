from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    phone_number: str = Field(min_length=10, max_length=20)
    username: str = Field(min_length=1, max_length=50)


class RegisterResponse(BaseModel):
    user_id: int
    phone_number: str
    username: str
    message: str


class LoginRequest(BaseModel):
    phone_number: str = Field(min_length=10, max_length=20)


class OTPVerifyRequest(BaseModel):
    phone_number: str = Field(min_length=10, max_length=20)
    otp: str = Field(min_length=6, max_length=6)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str