from fastapi import APIRouter

from app.api.public import announcement

public_router = APIRouter()

public_router.include_router(announcement.router, prefix="/announcements", tags=["Public – Announcements"])