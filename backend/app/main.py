from fastapi import Depends, FastAPI

from app.core.config import settings
from app.database.database import Base, engine
from app.dependencies import get_current_user
from app.models import User
from app.routers import auth_router


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)


Base.metadata.create_all(bind=engine)

app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "application": settings.app_name
    }


@app.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "user_id": current_user.user_id,
        "phone_number": current_user.phone_number,
        "username": current_user.username,
        "profile_picture": current_user.profile_picture,
        "status": current_user.status,
        "last_seen": current_user.last_seen
    }