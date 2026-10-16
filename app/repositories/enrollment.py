import math
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.enrollment import Enrollment
from app.models.student import Student
from app.repositories.base import BaseRepository


class EnrollmentRepository(BaseRepository[Enrollment]):
    def __init__(self, db: AsyncSession):
        super().__init__(Enrollment, db)

    async def get_by_student_and_course(
        self, student_id: int, course_id: int
    ) -> Enrollment | None:
        stmt = select(Enrollment).where(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_with_relations(self, enrollment_id: int) -> Enrollment | None:
        stmt = (
            select(Enrollment)
            .options(
                joinedload(Enrollment.student).joinedload(Student.user),
                joinedload(Enrollment.course),
            )
            .where(Enrollment.id == enrollment_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_enrollments(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        student_id: int | None = None,
        course_id: int | None = None,
    ):
        base = select(Enrollment)

        if student_id is not None:
            base = base.where(Enrollment.student_id == student_id)

        if course_id is not None:
            base = base.where(Enrollment.course_id == course_id)

        total = (
            await self.db.execute(select(func.count()).select_from(base.subquery()))
        ).scalar_one()

        stmt = (
            base.options(
                joinedload(Enrollment.student).joinedload(Student.user),
                joinedload(Enrollment.course),
            )
            .order_by(Enrollment.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        data = (await self.db.execute(stmt)).scalars().all()

        return {
            "data": data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": math.ceil(total / page_size) if total else 0,
        }

