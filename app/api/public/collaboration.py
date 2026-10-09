from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.collaboration import CollaborationRepository
from app.schemas.collaboration import CollaborationPagination, CollaborationRead
from app.services.collaboration_service import CollaborationService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> CollaborationService:
    return CollaborationService(CollaborationRepository(db))


@router.get("", response_model=CollaborationPagination)
async def list_public_collaborations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    service: CollaborationService = Depends(_service),
):
    return await service.list_published(
        page=page,
        page_size=page_size,
        search=search,
    )


@router.get("/{collaboration_id}", response_model=CollaborationRead)
async def get_public_collaboration(
    collaboration_id: int,
    service: CollaborationService = Depends(_service),
):
    return await service.get_published_by_id(collaboration_id)

