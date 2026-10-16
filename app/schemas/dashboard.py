from datetime import datetime
from pydantic import BaseModel


class RecentItem(BaseModel):
    id: int
    title: str
    created_at: datetime


class DashboardOverviewResponse(BaseModel):
    total_students: int
    total_faculty: int
    total_courses: int
    total_departments: int
    total_enrollments: int
    total_events: int
    total_announcements: int
    total_projects: int
    total_partners: int
    total_scholarships: int
    total_awards: int
    total_collaborations: int

    published_courses: int
    active_faculty: int
    published_events: int

    recent_announcements: list[RecentItem] = []
    recent_events: list[RecentItem] = []

