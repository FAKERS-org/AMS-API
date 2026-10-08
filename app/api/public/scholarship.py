from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.scholarship import ScholarshipRepository
from app.schemas.scholarship import ScholarshipPagination, ScholarshipRead
from app.services.scholarship_service import ScholarshipService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> ScholarshipService:
    return ScholarshipService(ScholarshipRepository(db))


@router.get("", response_model=ScholarshipPagination)
async def list_public_scholarships(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    service: ScholarshipService = Depends(_service),
):
    return await service.list_published(
        page=page,
        page_size=page_size,
        search=search,
    )


@router.get("/{scholarship_id}", response_model=ScholarshipRead)
async def get_public_scholarship(
    scholarship_id: int,
    service: ScholarshipService = Depends(_service),
):
    return await service.get_published_by_id(scholarship_id)

