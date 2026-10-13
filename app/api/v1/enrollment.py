from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role
from app.models.student import Student
from app.models.user import User
from app.repositories.enrollment import EnrollmentRepository
from app.schemas.enrollment import EnrollmentCreate, EnrollmentPagination, EnrollmentRead
from app.services.enrollment_service import EnrollmentService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> EnrollmentService:
    return EnrollmentService(EnrollmentRepository(db))


@router.get("", response_model=EnrollmentPagination)
async def list_enrollments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    student_id: int | None = Query(None),
    course_id: int | None = Query(None),
    service: EnrollmentService = Depends(_service),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_role = Role(current_user.role)
    if user_role in (Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF):
        return await service.list(
            page=page,
            page_size=page_size,
            student_id=student_id,
            course_id=course_id,
        )

    if user_role == Role.STUDENT:
        # A student can only view their own enrollments
        from sqlalchemy import select
        res = await db.execute(select(Student).where(Student.user_id == current_user.id))
        student = res.scalar_one_or_none()
        if not student:
            return {
                "data": [],
                "total": 0,
                "page": page,
                "page_size": page_size,
                "total_pages": 0,
            }
        return await service.list(
            page=page,
            page_size=page_size,
            student_id=student.id,
            course_id=course_id,
        )

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")


@router.get("/{enrollment_id}", response_model=EnrollmentRead)
async def get_enrollment(
    enrollment_id: int,
    service: EnrollmentService = Depends(_service),
    current_user: User = Depends(get_current_user),
):
    enrollment = await service.get_by_id(enrollment_id)
    user_role = Role(current_user.role)

    if user_role in (Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF):
        return enrollment

    if user_role == Role.STUDENT and enrollment.student and enrollment.student.user_id == current_user.id:
        return enrollment

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")


@router.post("", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
async def create_enrollment(
    data: EnrollmentCreate,
    service: EnrollmentService = Depends(_service),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_role = Role(current_user.role)

    if user_role in (Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF):
        return await service.enroll(data)

    if user_role == Role.STUDENT:
        from sqlalchemy import select
        res = await db.execute(select(Student).where(Student.user_id == current_user.id))
        student = res.scalar_one_or_none()
        if not student or student.id != data.student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only enroll for yourself",
            )
        return await service.enroll(data)

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_enrollment(
    enrollment_id: int,
    service: EnrollmentService = Depends(_service),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    enrollment = await service.get_by_id(enrollment_id)
    user_role = Role(current_user.role)

    if user_role in (Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF):
        await service.unenroll(enrollment_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    if user_role == Role.STUDENT:
        from sqlalchemy import select
        res = await db.execute(select(Student).where(Student.user_id == current_user.id))
        student = res.scalar_one_or_none()
        if student and enrollment.student_id == student.id:
            await service.unenroll(enrollment_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

