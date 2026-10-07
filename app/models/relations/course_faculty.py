import enum

from sqlalchemy import String, Enum as SAEnum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, IDMixin


class Semester(str, enum.Enum):
    FALL = "fall"
    SPRING = "spring"
    SUMMER = "summer"


class InstructorRole(str, enum.Enum):
    LEAD = "lead"          
    CO_INSTRUCTOR = "co"   
    TA = "ta"              
    GUEST = "guest"         


class CourseFaculty(IDMixin, TimestampMixin, Base):

    __tablename__ = "course_faculty"
    __table_args__ = (
        UniqueConstraint(
            "course_id", "faculty_id", "academic_year", "semester", "section",
            name="uq_course_faculty_assignment",
        ),
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), index=True
    )
    faculty_id: Mapped[int] = mapped_column(
        ForeignKey("faculty.id", ondelete="CASCADE"), index=True
    )

    academic_year: Mapped[str] = mapped_column(String(20))      
    semester: Mapped[Semester] = mapped_column(SAEnum(Semester))
    section: Mapped[str] = mapped_column(String(10), default="A") 
    role: Mapped[InstructorRole] = mapped_column(
        SAEnum(InstructorRole), default=InstructorRole.LEAD
    )

    course = relationship("Course", back_populates="faculty_assignments")
    faculty = relationship("Faculty", back_populates="course_assignments")
