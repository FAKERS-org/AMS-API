from sqlalchemy import select

from app.core.exceptions import AppException
from app.models.department import Department
from app.repositories.course import CourseRepository
from app.schemas.course import CourseCreate, CourseUpdate


class CourseService:
    def __init__(self, repo: CourseRepository):
        self.repo = repo

    async def setup_table(self):
        return [
            {"value": "title", "label": "Title", "type": "text"},
            {"value": "category", "label": "Category", "type": "text"},
            {"value": "code", "label": "Code", "type": "text"},
            {"value": "semester", "label": "Semester", "type": "text"},
            {"value": "year", "label": "Year", "type": "number"},
            {"value": "credit", "label": "Credit", "type": "number"},
            {"value": "actions", "label": "Actions", "type": "actions"},
        ]

    async def setup(self):
        dept_stmt = select(Department.id, Department.name)
        depts = (await self.repo.db.execute(dept_stmt)).all()
        categories = [{"value": d.id, "label": d.name} for d in depts]
        return {
            "name": "Course",
            "categories": categories,
            "fields": [
                {
                    "name": "title",
                    "value": "title",
                    "label": "Course Title",
                    "type": "text",
                    "is_required": True,
                },
                {
                    "name": "code_name",
                    "value": "code_name",
                    "label": "Course Code",
                    "type": "text",
                    "is_required": True,
                },
                {
                    "name": "credit",
                    "value": "credit",
                    "label": "Credit",
                    "type": "number",
                    "is_required": True,
                },
                {
                    "name": "year",
                    "value": "year",
                    "label": "Year",
                    "type": "number",
                    "is_required": True,
                },
                {
                    "name": "semester",
                    "value": "semester",
                    "label": "Semester",
                    "type": "select",
                    "options": [
                        {"label": "Semester 1", "value": "1"},
                        {"label": "Semester 2", "value": "2"},
                    ],
                },
                {
                    "name": "category_id",
                    "value": "category_id",
                    "label": "Category",
                    "type": "select",
                    "options": categories,
                },
            ],
        }

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

    async def list_all(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department_id: int | None = None,
        is_published: bool | None = None,
    ):
        return await self.repo.list_all(
            page=page,
            page_size=page_size,
            search=search,
            department_id=department_id,
            is_published=is_published,
        )

    async def get_by_id(self, course_id: int):
        course = await self.repo.get_with_relations(course_id)
        if not course:
            raise AppException(404, "Course not found")
        return course

    async def view(self, course_id: int):
        return await self.get_by_id(course_id)

    async def create(self, data: CourseCreate):
        existing = await self.repo.get_by_code(data.code)
        if existing:
            raise AppException(409, f"Course code '{data.code}' already exists")

        target_dept_id = data.department_id
        if target_dept_id is not None:
            dept = await self.repo.db.get(Department, target_dept_id)
            if not dept:
                raise AppException(404, f"Department with ID {target_dept_id} not found")

        create_dict = {
            "code": data.code,
            "title": data.title,
            "description": data.description,
            "credit_hours": data.credit_hours,
            "department_id": target_dept_id,
            "is_published": data.is_published,
        }

        created = await self.repo.create(create_dict)
        return await self.get_by_id(created.id)

    async def update(self, course_id: int, data: CourseUpdate):
        course = await self.repo.get_by_id(course_id)
        if not course:
            raise AppException(404, "Course not found")

        update_dict = {}
        if data.code is not None:
            existing = await self.repo.get_by_code(data.code)
            if existing and existing.id != course_id:
                raise AppException(409, f"Course code '{data.code}' already exists")
            update_dict["code"] = data.code

        if data.title is not None:
            update_dict["title"] = data.title
        if data.description is not None:
            update_dict["description"] = data.description
        if data.credit_hours is not None:
            update_dict["credit_hours"] = data.credit_hours
        if data.department_id is not None:
            dept = await self.repo.db.get(Department, data.department_id)
            if not dept:
                raise AppException(404, f"Department with ID {data.department_id} not found")
            update_dict["department_id"] = data.department_id
        if data.is_published is not None:
            update_dict["is_published"] = data.is_published

        if update_dict:
            await self.repo.update(course, update_dict)
        return await self.get_by_id(course_id)

    async def delete(self, course_id: int):
        course = await self.repo.get_by_id(course_id)
        if not course:
            raise AppException(404, "Course not found")
        await self.repo.delete(course)
