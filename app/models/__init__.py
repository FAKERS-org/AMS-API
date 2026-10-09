
from app.models.base import Base
from app.models.announcement import Announcement
from app.models.course import Course
from app.models.department import Department
from app.models.enrollment import Enrollment
from app.models.user import User
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.relations.course_faculty import CourseFaculty
from app.models.event import Event, EventCategory
from app.models.scholarship import Scholarship
from app.models.partner import Partner
from app.models.project import Project
from app.models.award import Award
from app.models.collaboration import Collaboration

__all__ = [
    "Base",
    "User",
    "Student",
    "Course",
    "Department",
    "Enrollment",
    "Faculty",
    "CourseFaculty",
    "Announcement",
    "Event",
    "EventCategory",
    "Scholarship",
    "Partner",
    "Project",
    "Award",
    "Collaboration",
]
