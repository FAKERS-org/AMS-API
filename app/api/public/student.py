from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.student import StudentRepository
from app.schemas.student import PublicStudentPagination, PublicStudentRead
from app.services.student_service import StudentService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> StudentService:
    return StudentService(StudentRepository(db))


@router.get("", response_model=PublicStudentPagination)
async def list_public_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    department_id: int | None = Query(None),
    year_level: int | None = Query(None),
    service: StudentService = Depends(_service),
):
    return await service.list_public(
        page=page,
        page_size=page_size,
        search=search,
        department_id=department_id,
        year_level=year_level,
    )


@router.get("/{student_id}", response_model=PublicStudentRead)
async def get_public_student(
    student_id: int,
    service: StudentService = Depends(_service),
):
    return await service.get_public_by_id(student_id)

