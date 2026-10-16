import time
from sqlalchemy import select

from app.core.exceptions import AppException
from app.core.permissions import Role
from app.core.security import hashed_password
from app.models.department import Department
from app.models.scholarship import Scholarship
from app.models.student import Student
from app.models.user import User
from app.repositories.student import StudentRepository
from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:
    def __init__(self, repo: StudentRepository):
        self.repo = repo

    async def setup_table(self):
        return [
            {"value": "name", "label": "Name", "type": "text"},
            {"value": "major", "label": "Major", "type": "text"},
            {"value": "year", "label": "Year", "type": "number"},
            {"value": "student_id_number", "label": "Student ID", "type": "text"},
            {"value": "photo", "label": "Photo", "type": "image"},
            {"value": "actions", "label": "Actions", "type": "actions"},
        ]

    async def setup(self):
        dept_stmt = select(Department.id, Department.name)
        depts = (await self.repo.db.execute(dept_stmt)).all()
        departments = [{"value": d.id, "label": d.name} for d in depts]

        sch_stmt = select(Scholarship.id, Scholarship.title)
        schs = (await self.repo.db.execute(sch_stmt)).all()
        scholarships = [{"value": s.id, "label": s.title} for s in schs]

        return {
            "departments": departments,
            "scholarships": scholarships,
            "yearOptions": [
                {"value": 1, "label": "Year 1"},
                {"value": 2, "label": "Year 2"},
                {"value": 3, "label": "Year 3"},
                {"value": 4, "label": "Year 4"},
            ],
        }

    async def list_public(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department_id: int | None = None,
        year_level: int | None = None,
    ):
        return await self.repo.get_public_list(
            page=page,
            page_size=page_size,
            search=search,
            department_id=department_id,
            year_level=year_level,
        )

    async def get_public_by_id(self, student_id: int):
        student = await self.repo.get_public_by_id(student_id)
        if not student:
            raise AppException(404, "Student not found")
        return student

    async def list_all(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        department_id: int | None = None,
        year_level: int | None = None,
    ):
        return await self.repo.list_all(
            page=page,
            page_size=page_size,
            search=search,
            department_id=department_id,
            year_level=year_level,
        )

    async def get_by_id(self, student_id: int):
        student = await self.repo.get_with_relations(student_id)
        if not student:
            raise AppException(404, "Student not found")
        return student

    async def view(self, student_id: int):
        return await self.get_by_id(student_id)


    async def create(self, data: StudentCreate):
        full_name = data.full_name or data.name or "Student"
        year_level = data.year or data.year_level or 1

        student_id_number = data.student_id_number
        if not student_id_number:
            student_id_number = f"STU{int(time.time() * 1000) % 10000000:07d}"

        # Check unique student_id_number
        existing_sid = await self.repo.get_by_student_id_number(student_id_number)
        if existing_sid:
            raise AppException(409, f"Student ID '{student_id_number}' already in use")

        # Resolve department
        target_department_id = data.department_id
        if target_department_id is None and data.major:
            dept_res = await self.repo.db.execute(
                select(Department).where(Department.name.ilike(f"%{data.major}%"))
            )
            matched_dept = dept_res.scalar_one_or_none()
            if matched_dept:
                target_department_id = matched_dept.id

        if target_department_id is not None:
            dept = await self.repo.db.get(Department, target_department_id)
            if not dept:
                raise AppException(404, f"Department with ID {target_department_id} not found")

        target_user_id = data.user_id if (data.user_id and data.user_id > 0) else None

        if target_user_id is None:
            email_val = str(data.email) if data.email else f"{full_name.lower().replace(' ', '.')}.{int(time.time())%10000}@student.university.edu"
            password_val = data.password or "Student123!"

            stmt = select(User).where(User.email == email_val)
            existing_user = (await self.repo.db.execute(stmt)).scalar_one_or_none()
            if existing_user:
                email_val = f"{full_name.lower().replace(' ', '.')}.{int(time.time() * 1000) % 100000}@student.university.edu"

            new_user = User(
                email=email_val,
                hashed_password=hashed_password(password_val),
                full_name=full_name,
                role=Role.STUDENT,
                is_active=True,
            )
            self.repo.db.add(new_user)
            await self.repo.db.flush()
            await self.repo.db.refresh(new_user)
            target_user_id = new_user.id
        else:
            existing_user = await self.repo.db.get(User, target_user_id)
            if not existing_user:
                raise AppException(404, f"User with ID {target_user_id} not found")
            existing_student = await self.repo.get_by_user_id(target_user_id)
            if existing_student:
                raise AppException(409, "User already has a student profile")

        student_dict = {
            "user_id": target_user_id,
            "student_id_number": student_id_number,
            "department_id": target_department_id,
            "year_level": year_level,
            "date_of_birth": data.date_of_birth,
        }

        created = await self.repo.create(student_dict)
        return await self.get_by_id(created.id)

    async def update(self, student_id: int, data: StudentUpdate):
        student = await self.repo.get_by_id(student_id)
        if not student:
            raise AppException(404, "Student not found")

        update_dict = {}
        if data.year or data.year_level:
            update_dict["year_level"] = data.year or data.year_level
        if data.date_of_birth is not None:
            update_dict["date_of_birth"] = data.date_of_birth

        target_dept_id = data.department_id
        if target_dept_id is None and data.major:
            dept_res = await self.repo.db.execute(
                select(Department).where(Department.name.ilike(f"%{data.major}%"))
            )
            matched_dept = dept_res.scalar_one_or_none()
            if matched_dept:
                target_dept_id = matched_dept.id

        if target_dept_id is not None:
            dept = await self.repo.db.get(Department, target_dept_id)
            if not dept:
                raise AppException(404, f"Department with ID {target_dept_id} not found")
            update_dict["department_id"] = target_dept_id

        if update_dict:
            await self.repo.update(student, update_dict)

        # Update user full_name if name provided
        name_val = data.full_name or data.name
        if name_val and student.user_id:
            user = await self.repo.db.get(User, student.user_id)
            if user:
                user.full_name = name_val
                await self.repo.db.flush()

        return await self.get_by_id(student_id)

    async def delete(self, student_id: int):
        student = await self.repo.get_by_id(student_id)
        if not student:
            raise AppException(404, "Student not found")
        await self.repo.delete(student)
