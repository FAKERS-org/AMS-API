from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.faculty import FacultyRepository
from app.schemas.faculty import PublicFacultyDetailRead, PublicFacultyPagination
from app.services.faculty_service import FacultyService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> FacultyService:
    return FacultyService(FacultyRepository(db))


@router.get("", response_model=PublicFacultyPagination)
async def list_public_faculty(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    department_id: int | None = Query(None),
    service: FacultyService = Depends(_service),
):
    return await service.list_public(
        page=page,
        page_size=page_size,
        search=search,
        department_id=department_id,
    )


@router.get("/{faculty_id}", response_model=PublicFacultyDetailRead)
async def get_public_faculty(
    faculty_id: int,
    service: FacultyService = Depends(_service),
):
    return await service.get_public_by_id(faculty_id)

