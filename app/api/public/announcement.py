from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.announcement import AnnouncementRepository
from app.schemas.announcement import AnnouncementRead
from app.services.announcement_service import AnnouncementService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> AnnouncementService:
    return AnnouncementService(AnnouncementRepository(db))

@router.get("")
async def list_public_announcements(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: AnnouncementService = Depends(_service),
):
    return await service.list_published(page=page, page_size=page_size)