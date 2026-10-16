from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.department import DepartmentRepository
from app.schemas.department import DepartmentDetailRead, DepartmentPagination, DepartmentRead
from app.services.department_service import DepartmentService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> DepartmentService:
    return DepartmentService(DepartmentRepository(db))


@router.get("", response_model=DepartmentPagination)
async def list_public_departments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    service: DepartmentService = Depends(_service),
):
    return await service.list(
        page=page,
        page_size=page_size,
        search=search,
    )


@router.get("/{department_id}", response_model=DepartmentDetailRead)
async def get_public_department(
    department_id: int,
    service: DepartmentService = Depends(_service),
):
    return await service.get_detail(department_id)

