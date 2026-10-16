import time
from datetime import date
from sqlalchemy import select

from app.core.exceptions import AppException
from app.core.permissions import Role
from app.core.security import hashed_password
from app.models.course import Course
from app.models.department import Department
from app.models.faculty import Faculty, FacultyTitle
from app.models.relations.course_faculty import CourseFaculty
from app.models.user import User
from app.repositories.faculty import FacultyRepository
from app.schemas.faculty import CourseFacultyCreate, FacultyCreate, FacultyUpdate


class FacultyService:
    def __init__(self, repo: FacultyRepository):
        self.repo = repo

    async def setup_table(self):
        return [
            {"value": "name", "label": "Name", "type": "text"},
            {"value": "education", "label": "Education", "type": "text"},
            {"value": "email", "label": "Email", "type": "text"},
            {"value": "courses", "label": "Courses", "type": "multi-select"},
            {"value": "role", "label": "Role", "type": "select"},
            {"value": "ongoing_projects", "label": "Ongoing Projects", "type": "multi-select"},
            {"value": "photo", "label": "Photo", "type": "image"},
            {"value": "actions", "label": "Actions", "type": "actions"},
        ]

    async def setup(self):
        dept_stmt = select(Department.id, Department.name)
        depts = (await self.repo.db.execute(dept_stmt)).all()
        departments = [{"value": d.id, "label": d.name} for d in depts]

        course_stmt = select(Course.id, Course.title)
        courses = (await self.repo.db.execute(course_stmt)).all()
        course_options = [{"value": c.id, "label": c.title} for c in courses]

        return {
            "name": "Faculty",
            "departments": departments,
            "courses": course_options,
            "fields": [
                {"name": "name", "value": "name", "type": "text", "label": "Name", "is_required": True},
                {"name": "email", "value": "email", "type": "text", "label": "Email", "is_required": True},
                {
                    "name": "department_id",
                    "value": "department_id",
                    "type": "select",
                    "label": "Department",
                    "options": departments,
                    "is_required": True,
                },
                {"name": "specialization", "value": "specialization", "type": "text", "label": "Specialization"},
                {
                    "name": "title",
                    "value": "title",
                    "type": "select",
                    "label": "Title",
                    "options": [
                        {"value": "assistant_professor", "label": "Assistant Professor"},
                        {"value": "associate_professor", "label": "Associate Professor"},
                        {"value": "professor", "label": "Professor"},
                        {"value": "lecturer", "label": "Lecturer"},
                        {"value": "adjunct", "label": "Adjunct"},
                    ],
                },
            ],
        }

    async def list_public(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department_id: int | None = None,
    ):
        return await self.repo.get_public_list(
            page=page,
            page_size=page_size,
            search=search,
            department_id=department_id,
        )

    async def get_public_by_id(self, faculty_id: int):
        faculty = await self.repo.get_public_by_id(faculty_id)
        if not faculty:
            raise AppException(404, "Faculty member not found")
        return faculty

    async def list_all(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department_id: int | None = None,
        is_active: bool | None = None,
    ):
        return await self.repo.list_all(
            page=page,
            page_size=page_size,
            search=search,
            department_id=department_id,
            is_active=is_active,
        )

    async def get_by_id(self, faculty_id: int):
        faculty = await self.repo.get_with_relations(faculty_id)
        if not faculty:
            raise AppException(404, "Faculty member not found")
        return faculty

    async def view(self, faculty_id: int):
        return await self.get_by_id(faculty_id)

    async def create(self, data: FacultyCreate):
        full_name = data.full_name or data.name or "Faculty Member"
        employee_id = data.employee_id or f"EMP{int(time.time() * 1000) % 10000000:07d}"
        password_val = data.password or "Faculty123!"
        hire_date_val = data.hire_date or date.today()

        if await self.repo.get_by_employee_id(employee_id):
            raise AppException(409, f"Employee ID '{employee_id}' already in use")

        dept_id = data.department_id
        if dept_id is None:
            first_dept = (await self.repo.db.execute(select(Department.id).limit(1))).scalar_one_or_none()
            dept_id = first_dept if first_dept else 1

        dept = await self.repo.db.get(Department, dept_id)
        if not dept:
            raise AppException(404, f"Department with ID {dept_id} not found")

        stmt = select(User).where(User.email == str(data.email))
        user = (await self.repo.db.execute(stmt)).scalar_one_or_none()
        if user:
            raise AppException(409, f"Email '{data.email}' already registered")

        new_user = User(
            email=str(data.email),
            hashed_password=hashed_password(password_val),
            full_name=full_name,
            role=Role.FACULTY,
            is_active=True,
        )
        self.repo.db.add(new_user)
        await self.repo.db.flush()
        await self.repo.db.refresh(new_user)

        faculty_dict = {
            "user_id": new_user.id,
            "department_id": dept_id,
            "employee_id": employee_id,
            "title": data.title,
            "specialization": data.specialization,
            "bio": data.bio,
            "office_location": data.office_location,
            "phone": data.phone,
            "hire_date": hire_date_val,
            "is_active": True,
        }

        created = await self.repo.create(faculty_dict)
        return await self.get_by_id(created.id)

    async def update(self, faculty_id: int, data: FacultyUpdate):
        faculty = await self.repo.get_by_id(faculty_id)
        if not faculty:
            raise AppException(404, "Faculty member not found")

        update_dict = {}
        if data.title is not None:
            update_dict["title"] = data.title
        if data.specialization is not None:
            update_dict["specialization"] = data.specialization
        if data.bio is not None:
            update_dict["bio"] = data.bio
        if data.office_location is not None:
            update_dict["office_location"] = data.office_location
        if data.phone is not None:
            update_dict["phone"] = data.phone
        if data.is_active is not None:
            update_dict["is_active"] = data.is_active
        if data.department_id is not None:
            dept = await self.repo.db.get(Department, data.department_id)
            if not dept:
                raise AppException(404, f"Department with ID {data.department_id} not found")
            update_dict["department_id"] = data.department_id

        if update_dict:
            await self.repo.update(faculty, update_dict)

        name_val = data.full_name or data.name
        if name_val and faculty.user_id:
            user = await self.repo.db.get(User, faculty.user_id)
            if user:
                user.full_name = name_val
                await self.repo.db.flush()

        return await self.get_by_id(faculty_id)

    async def delete(self, faculty_id: int):
        faculty = await self.repo.get_by_id(faculty_id)
        if not faculty:
            raise AppException(404, "Faculty member not found")
        await self.repo.delete(faculty)

    async def assign_course(self, faculty_id: int, data: CourseFacultyCreate):
        faculty = await self.repo.get_by_id(faculty_id)
        if not faculty:
            raise AppException(404, "Faculty member not found")

        course = await self.repo.db.get(Course, data.course_id)
        if not course:
            raise AppException(404, f"Course with ID {data.course_id} not found")

        # Check existing assignment
        stmt = select(CourseFaculty).where(
            CourseFaculty.faculty_id == faculty_id,
            CourseFaculty.course_id == data.course_id,
            CourseFaculty.academic_year == data.academic_year,
            CourseFaculty.semester == data.semester,
            CourseFaculty.section == data.section,
        )
        existing = (await self.repo.db.execute(stmt)).scalar_one_or_none()
        if existing:
            raise AppException(409, "Course section already assigned to this faculty member for this term")

        assignment = CourseFaculty(
            faculty_id=faculty_id,
            course_id=data.course_id,
            academic_year=data.academic_year,
            semester=data.semester,
            section=data.section,
            role=data.role,
        )
        await self.repo.assign_course(assignment)
        return await self.repo.get_assignment(assignment.id)

    async def remove_assignment(self, faculty_id: int, assignment_id: int):
        assignment = await self.repo.get_assignment(assignment_id)
        if not assignment or assignment.faculty_id != faculty_id:
            raise AppException(404, "Assignment not found")
        await self.repo.delete_assignment(assignment)
