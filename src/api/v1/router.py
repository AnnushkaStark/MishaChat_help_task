from fastapi import APIRouter

from api.v1.endpoints.auth import router as auth_router
from api.v1.endpoints.chat import router as chat_router
from api.v1.endpoints.message import router as message_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(chat_router, prefix="/chat", tags=["Chat"])
api_router.include_router(
    message_router, prefix="/messages", tags=["Messages"]
)
