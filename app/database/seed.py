"""
AMS Database Seeder
Run: python -m app.database.seed
"""
import asyncio
import json
import logging
from datetime import date, datetime
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import Role
from app.core.security import hashed_password as hash_password
from app.core.database import AsyncSessionLocal, engine
from app.models.base import Base
from app.models.announcement import Announcement
from app.models.award import Award
from app.models.collaboration import Collaboration
from app.models.course import Course
from app.models.department import Department
from app.models.enrollment import Enrollment
from app.models.event import Event
from app.models.faculty import Faculty, FacultyTitle
from app.models.partner import Partner
from app.models.project import Project
from app.models.relations.course_faculty import CourseFaculty, Semester, InstructorRole
from app.models.scholarship import Scholarship
from app.models.student import Student
from app.models.user import User

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

SEEDS_DIR = Path(__file__).parent / "seeds"


def load(filename: str) -> list[dict]:
    with open(SEEDS_DIR / filename) as f:
        return json.load(f)


# ─── 1. Departments ──────────────────────────────────────────────────────────

async def seed_departments(db: AsyncSession) -> dict[str, int]:
    """Returns {name: id}"""
    data = load("departments.json")
    dept_map: dict[str, int] = {}
    for item in data:
        existing = await db.execute(
            __import__("sqlalchemy").select(Department).where(Department.name == item["name"])
        )
        dept = existing.scalar_one_or_none()
        if not dept:
            dept = Department(name=item["name"])
            db.add(dept)
            await db.flush()
            log.info(f"  + Department: {dept.name}")
        dept_map[dept.name] = dept.id
    return dept_map


# ─── 2. Users ─────────────────────────────────────────────────────────────────

async def seed_users(db: AsyncSession) -> dict[str, int]:
    """Returns {email: id}"""
    from sqlalchemy import select
    data = load("users.json")
    user_map: dict[str, int] = {}
    for item in data:
        existing = await db.execute(select(User).where(User.email == item["email"]))
        user = existing.scalar_one_or_none()
        if not user:
            user = User(
                email=item["email"],
                full_name=item["full_name"],
                hashed_password=hash_password(item["password"]),
                role=Role(item["role"]),
                is_active=True,
            )
            db.add(user)
            await db.flush()
            log.info(f"  + User: {user.email} ({user.role})")
        user_map[user.email] = user.id
    return user_map


# ─── 3. Faculty ───────────────────────────────────────────────────────────────

async def seed_faculty(db: AsyncSession, user_map: dict[str, int], dept_map: dict[str, int]) -> dict[str, int]:
    """Returns {email: faculty_id}"""
    from sqlalchemy import select
    data = load("faculty.json")
    faculty_map: dict[str, int] = {}
    for item in data:
        user_id = user_map.get(item["email"])
        if not user_id:
            log.warning(f"  ! No user found for faculty email: {item['email']}")
            continue
        existing = await db.execute(select(Faculty).where(Faculty.user_id == user_id))
        fac = existing.scalar_one_or_none()
        if not fac:
            dept_id = dept_map.get(item["department"])
            fac = Faculty(
                user_id=user_id,
                employee_id=item["employee_id"],
                department_id=dept_id,
                title=FacultyTitle(item["title"]),
                specialization=item.get("specialization"),
                bio=item.get("bio"),
                office_location=item.get("office_location"),
                phone=item.get("phone"),
                hire_date=date.fromisoformat(item["hire_date"]),
                is_active=True,
            )
            db.add(fac)
            await db.flush()
            log.info(f"  + Faculty: {item['email']}")
        faculty_map[item["email"]] = fac.id
    return faculty_map


# ─── 4. Students ──────────────────────────────────────────────────────────────

async def seed_students(db: AsyncSession, user_map: dict[str, int], dept_map: dict[str, int]) -> dict[str, int]:
    """Returns {email: student_id}"""
    from sqlalchemy import select
    data = load("student.json")
    student_map: dict[str, int] = {}
    for idx, item in enumerate(data, start=1):
        user_id = user_map.get(item["email"])
        if not user_id:
            log.warning(f"  ! No user found for student email: {item['email']}")
            continue
        existing = await db.execute(select(Student).where(Student.user_id == user_id))
        stu = existing.scalar_one_or_none()
        if not stu:
            dept_id = dept_map.get(item.get("department", ""))
            sid = f"ITC-{date.today().year}-{idx:04d}"
            stu = Student(
                user_id=user_id,
                student_id_number=sid,
                date_of_birth=date.fromisoformat(item["date_of_birth"]) if item.get("date_of_birth") else None,
                department_id=dept_id,
                year_level=item.get("year_level", 1),
            )
            db.add(stu)
            await db.flush()
            log.info(f"  + Student: {item['email']} ({sid})")
        student_map[item["email"]] = stu.id
    return student_map


# ─── 5. Courses ───────────────────────────────────────────────────────────────

async def seed_courses(db: AsyncSession, dept_map: dict[str, int]) -> dict[str, int]:
    """Returns {code: course_id}"""
    from sqlalchemy import select
    data = load("courses.json")
    course_map: dict[str, int] = {}
    for item in data:
        existing = await db.execute(select(Course).where(Course.code == item["code"]))
        course = existing.scalar_one_or_none()
        if not course:
            dept_id = dept_map.get(item.get("department", ""))
            course = Course(
                code=item["code"],
                title=item["title"],
                description=item.get("description"),
                credit_hours=int(item.get("credit_hours", 3)),
                department_id=dept_id,
                is_published=True,
            )
            db.add(course)
            await db.flush()
            log.info(f"  + Course: {item['code']} – {item['title']}")
        course_map[item["code"]] = course.id
    return course_map


# ─── 6. Course–Faculty assignments ───────────────────────────────────────────

async def seed_course_faculty(
    db: AsyncSession,
    faculty_map: dict[str, int],
    course_map: dict[str, int],
) -> None:
    from sqlalchemy import select
    data = load("course_faculty.json")
    for item in data:
        fid = faculty_map.get(item["faculty_email"])
        cid = course_map.get(item["course_code"])
        if not fid or not cid:
            log.warning(f"  ! Skipping assignment: {item['faculty_email']} → {item['course_code']}")
            continue
        existing = await db.execute(
            select(CourseFaculty).where(
                CourseFaculty.faculty_id == fid,
                CourseFaculty.course_id == cid,
                CourseFaculty.academic_year == item["academic_year"],
                CourseFaculty.semester == Semester(item["semester"]),
                CourseFaculty.section == item.get("section", "A"),
            )
        )
        if not existing.scalar_one_or_none():
            cf = CourseFaculty(
                faculty_id=fid,
                course_id=cid,
                academic_year=item["academic_year"],
                semester=Semester(item["semester"]),
                section=item.get("section", "A"),
                role=InstructorRole(item.get("role", "lead")),
            )
            db.add(cf)
            log.info(f"  + Assignment: {item['faculty_email']} → {item['course_code']}")


# ─── 7. Events ───────────────────────────────────────────────────────────────

async def seed_events(db: AsyncSession) -> None:
    from sqlalchemy import select
    from app.models.event import EventCategory
    data = load("events.json")
    for item in data:
        existing = await db.execute(select(Event).where(Event.title == item["title"]))
        if not existing.scalar_one_or_none():
            db.add(Event(
                title=item["title"],
                category=EventCategory(item.get("category", "events")),
                description=item.get("description"),
                preview=item.get("preview"),
                published_by=item.get("published_by"),
                location=item.get("location"),
                tag=item.get("tag"),
                photo=item.get("photo"),
                event_url=item.get("event_url"),
                published_date=datetime.fromisoformat(item["published_date"]) if item.get("published_date") else None,
                status=item.get("status", "published"),
                is_published=item.get("is_published", True),
            ))
            log.info(f"  + Event: {item['title']}")


# ─── 8. Awards ───────────────────────────────────────────────────────────────

async def seed_awards(db: AsyncSession, student_map: dict[str, int]) -> None:
    from sqlalchemy import select
    data = load("awards.json")
    for item in data:
        existing = await db.execute(select(Award).where(Award.title == item["title"]))
        if not existing.scalar_one_or_none():
            student_id = student_map.get(item.get("student_email", ""))
            db.add(Award(
                title=item["title"],
                description=item.get("description"),
                achievement=item.get("achievement"),
                imagepath=item.get("imagepath"),
                recipient_name=item.get("recipient_name"),
                student_id=student_id,
                award_date=datetime.fromisoformat(item["award_date"]) if item.get("award_date") else None,
                is_published=item.get("is_published", True),
            ))
            log.info(f"  + Award: {item['title']}")


# ─── 9. Scholarships ─────────────────────────────────────────────────────────

async def seed_scholarships(db: AsyncSession) -> None:
    from sqlalchemy import select
    data = load("scholarships.json")
    for item in data:
        existing = await db.execute(select(Scholarship).where(Scholarship.title == item["title"]))
        if not existing.scalar_one_or_none():
            db.add(Scholarship(
                title=item["title"],
                description=item.get("description"),
                amount=item.get("amount"),
                duration=item.get("duration"),
                eligibility=item.get("eligibility"),
                application_process=item.get("application_process"),
                contact_office=item.get("contact_office"),
                contact_email=item.get("contact_email"),
                contact_phone=item.get("contact_phone"),
                deadline=datetime.fromisoformat(item["deadline"]) if item.get("deadline") else None,
                is_published=item.get("is_published", True),
            ))
            log.info(f"  + Scholarship: {item['title']}")


# ─── 10. Partners ────────────────────────────────────────────────────────────

async def seed_partners(db: AsyncSession) -> None:
    from sqlalchemy import select
    data = load("partners.json")
    for item in data:
        existing = await db.execute(select(Partner).where(Partner.name == item["name"]))
        if not existing.scalar_one_or_none():
            db.add(Partner(
                name=item["name"],
                description=item.get("description"),
                photo=item.get("photo"),
                website_url=item.get("website_url"),
                partner_type=item.get("partner_type"),
                is_active=item.get("is_active", True),
            ))
            log.info(f"  + Partner: {item['name']}")


# ─── 11. Projects ─────────────────────────────────────────────────────────────

async def seed_projects(db: AsyncSession) -> None:
    from sqlalchemy import select
    data = load("projects.json")
    for item in data:
        existing = await db.execute(select(Project).where(Project.title == item["title"]))
        if not existing.scalar_one_or_none():
            db.add(Project(
                title=item["title"],
                description=item.get("description"),
                partner=item.get("partner"),
                duration=item.get("duration"),
                funding=item.get("funding"),
                investigators=item.get("investigators"),
                students=item.get("students"),
                status=item.get("status", "ongoing"),
                is_published=item.get("is_published", True),
            ))
            log.info(f"  + Project: {item['title']}")


# ─── 12. Collaborations ───────────────────────────────────────────────────────

async def seed_collaborations(db: AsyncSession) -> None:
    from sqlalchemy import select
    data = load("collaborations.json")
    for item in data:
        existing = await db.execute(select(Collaboration).where(Collaboration.title == item["title"]))
        if not existing.scalar_one_or_none():
            db.add(Collaboration(
                title=item["title"],
                description=item.get("description"),
                duration=item.get("duration"),
                funding=item.get("funding"),
                objective=item.get("objective"),
                tag=item.get("tag"),
                image=item.get("image"),
                url=item.get("url"),
                is_published=item.get("is_published", True),
            ))
            log.info(f"  + Collaboration: {item['title']}")


# ─── 13. Announcements ────────────────────────────────────────────────────────

async def seed_announcements(db: AsyncSession, user_map: dict[str, int]) -> None:
    from sqlalchemy import select
    data = load("announcements.json")
    for item in data:
        existing = await db.execute(select(Announcement).where(Announcement.title == item["title"]))
        if not existing.scalar_one_or_none():
            author_id = user_map.get(item.get("author_email", ""), 1)
            db.add(Announcement(
                title=item["title"],
                content=item["content"],
                author_id=author_id,
                is_published=item.get("is_published", True),
                is_pinned=item.get("is_pinned", False),
            ))
            log.info(f"  + Announcement: {item['title']}")


# ─── Main runner ──────────────────────────────────────────────────────────────

async def run():
    log.info("🌱 Starting AMS database seeding...\n")

    async with AsyncSessionLocal() as db:
        log.info("📦 Departments")
        dept_map = await seed_departments(db)
        await db.commit()

        log.info("\n👤 Users")
        user_map = await seed_users(db)
        await db.commit()

        log.info("\n🎓 Faculty")
        faculty_map = await seed_faculty(db, user_map, dept_map)
        await db.commit()

        log.info("\n🧑‍🎓 Students")
        student_map = await seed_students(db, user_map, dept_map)
        await db.commit()

        log.info("\n📚 Courses")
        course_map = await seed_courses(db, dept_map)
        await db.commit()

        log.info("\n🔗 Course–Faculty Assignments")
        await seed_course_faculty(db, faculty_map, course_map)
        await db.commit()

        log.info("\n📅 Events")
        await seed_events(db)
        await db.commit()

        log.info("\n🏆 Awards")
        await seed_awards(db, student_map)
        await db.commit()

        log.info("\n💰 Scholarships")
        await seed_scholarships(db)
        await db.commit()

        log.info("\n🤝 Partners")
        await seed_partners(db)
        await db.commit()

        log.info("\n🔬 Projects")
        await seed_projects(db)
        await db.commit()

        log.info("\n🌐 Collaborations")
        await seed_collaborations(db)
        await db.commit()

        log.info("\n📢 Announcements")
        await seed_announcements(db, user_map)
        await db.commit()

    log.info("\n✅ Seeding complete!")


if __name__ == "__main__":
    asyncio.run(run())

