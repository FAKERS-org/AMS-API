from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.award import AwardRepository
from app.schemas.award import AwardPagination, AwardRead
from app.services.award_service import AwardService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> AwardService:
    return AwardService(AwardRepository(db))


@router.get("", response_model=AwardPagination)
async def list_public_awards(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    service: AwardService = Depends(_service),
):
    return await service.list_published(
        page=page,
        page_size=page_size,
        search=search,
    )


@router.get("/{award_id}", response_model=AwardRead)
async def get_public_award(
    award_id: int,
    service: AwardService = Depends(_service),
):
    return await service.get_published_by_id(award_id)

