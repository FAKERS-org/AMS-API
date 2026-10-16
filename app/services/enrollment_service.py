from app.core.exceptions import AppException
from app.models.course import Course
from app.models.student import Student
from app.repositories.enrollment import EnrollmentRepository
from app.schemas.enrollment import EnrollmentCreate


class EnrollmentService:
    def __init__(self, repo: EnrollmentRepository):
        self.repo = repo

    async def list(
        self,
        page: int = 1,
        page_size: int = 20,
        student_id: int | None = None,
        course_id: int | None = None,
    ):
        return await self.repo.list_enrollments(
            page=page,
            page_size=page_size,
            student_id=student_id,
            course_id=course_id,
        )

    async def get_by_id(self, enrollment_id: int):
        enrollment = await self.repo.get_by_id_with_relations(enrollment_id)
        if not enrollment:
            raise AppException(404, "Enrollment not found")
        return enrollment

    async def enroll(self, data: EnrollmentCreate):
        # Verify student exists
        student = await self.repo.db.get(Student, data.student_id)
        if not student:
            raise AppException(404, f"Student with ID {data.student_id} not found")

        # Verify course exists
        course = await self.repo.db.get(Course, data.course_id)
        if not course:
            raise AppException(404, f"Course with ID {data.course_id} not found")

        # Check duplicate
        existing = await self.repo.get_by_student_and_course(
            student_id=data.student_id,
            course_id=data.course_id,
        )
        if existing:
            raise AppException(409, "Student is already enrolled in this course")

        created = await self.repo.create(data.model_dump())
        return await self.repo.get_by_id_with_relations(created.id)

    async def unenroll(self, enrollment_id: int):
        enrollment = await self.repo.get_by_id(enrollment_id)
        if not enrollment:
            raise AppException(404, "Enrollment not found")
        await self.repo.delete(enrollment)

