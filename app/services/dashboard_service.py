from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.announcement import Announcement
from app.models.award import Award
from app.models.collaboration import Collaboration
from app.models.course import Course
from app.models.department import Department
from app.models.enrollment import Enrollment
from app.models.event import Event
from app.models.faculty import Faculty
from app.models.partner import Partner
from app.models.project import Project
from app.models.scholarship import Scholarship
from app.models.student import Student
from app.schemas.dashboard import DashboardOverviewResponse, RecentItem


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_overview(self) -> DashboardOverviewResponse:
        total_students = (await self.db.execute(select(func.count(Student.id)))).scalar_one() or 0
        total_faculty = (await self.db.execute(select(func.count(Faculty.id)))).scalar_one() or 0
        active_faculty = (
            await self.db.execute(select(func.count(Faculty.id)).where(Faculty.is_active.is_(True)))
        ).scalar_one() or 0

        total_courses = (await self.db.execute(select(func.count(Course.id)))).scalar_one() or 0
        published_courses = (
            await self.db.execute(select(func.count(Course.id)).where(Course.is_published.is_(True)))
        ).scalar_one() or 0

        total_departments = (await self.db.execute(select(func.count(Department.id)))).scalar_one() or 0
        total_enrollments = (await self.db.execute(select(func.count(Enrollment.id)))).scalar_one() or 0

        total_events = (await self.db.execute(select(func.count(Event.id)))).scalar_one() or 0
        published_events = (
            await self.db.execute(select(func.count(Event.id)).where(Event.is_published.is_(True)))
        ).scalar_one() or 0

        total_announcements = (await self.db.execute(select(func.count(Announcement.id)))).scalar_one() or 0
        total_projects = (await self.db.execute(select(func.count(Project.id)))).scalar_one() or 0
        total_partners = (await self.db.execute(select(func.count(Partner.id)))).scalar_one() or 0
        total_scholarships = (await self.db.execute(select(func.count(Scholarship.id)))).scalar_one() or 0
        total_awards = (await self.db.execute(select(func.count(Award.id)))).scalar_one() or 0
        total_collaborations = (await self.db.execute(select(func.count(Collaboration.id)))).scalar_one() or 0

        # Recent announcements
        ann_res = await self.db.execute(
            select(Announcement.id, Announcement.title, Announcement.created_at)
            .order_by(Announcement.created_at.desc())
            .limit(5)
        )
        recent_announcements = [
            RecentItem(id=row.id, title=row.title, created_at=row.created_at)
            for row in ann_res.all()
        ]

        # Recent events
        ev_res = await self.db.execute(
            select(Event.id, Event.title, Event.created_at)
            .order_by(Event.created_at.desc())
            .limit(5)
        )
        recent_events = [
            RecentItem(id=row.id, title=row.title, created_at=row.created_at)
            for row in ev_res.all()
        ]

        return DashboardOverviewResponse(
            total_students=total_students,
            total_faculty=total_faculty,
            total_courses=total_courses,
            total_departments=total_departments,
            total_enrollments=total_enrollments,
            total_events=total_events,
            total_announcements=total_announcements,
            total_projects=total_projects,
            total_partners=total_partners,
            total_scholarships=total_scholarships,
            total_awards=total_awards,
            total_collaborations=total_collaborations,
            published_courses=published_courses,
            active_faculty=active_faculty,
            published_events=published_events,
            recent_announcements=recent_announcements,
            recent_events=recent_events,
        )

