from app.routers.auth import router as auth_router
from app.routers.contacts import router as contacts_router
from app.routers.messages import router as messages_router

__all__ = [
    "auth_router",
    "contacts_router",
    "messages_router",
]