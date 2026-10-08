from app.core.exceptions import AppException
from app.repositories.course import CourseRepository


class CourseService:
    def __init__(self, repo: CourseRepository):
        self.repo = repo

    async def list_published(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department_id: int | None = None,
    ):
        return await self.repo.get_published(
            page=page,
            page_size=page_size,
            search=search,
            department_id=department_id,
        )

    async def get_published_by_id(self, course_id: int):
        course = await self.repo.get_published_by_id(course_id)
        if not course:
            raise AppException(404, "Course not found")
        return course

