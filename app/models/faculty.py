import enum
from datetime import date

from sqlalchemy import String, Date, Enum as SAEnum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, IDMixin


class FacultyTitle(str, enum.Enum):
    LECTURER = "lecturer"
    ASSISTANT_PROFESSOR = "assistant_professor"
    ASSOCIATE_PROFESSOR = "associate_professor"
    PROFESSOR = "professor"
    ADJUNCT = "adjunct"
    EMERITUS = "emeritus"


class Faculty(IDMixin, TimestampMixin, Base):
    __tablename__ = "faculty"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True
    )
    employee_id: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"), index=True, nullable=False
    )
    title: Mapped[FacultyTitle] = mapped_column(
        SAEnum(FacultyTitle), default=FacultyTitle.LECTURER
    )
    specialization: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)

    office_location: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)

    hire_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    user = relationship("User", back_populates="faculty_profile")
    department = relationship("Department", back_populates="faculty")
    course_assignments = relationship(
        "CourseFaculty",
        back_populates="faculty",
        cascade="all, delete-orphan",
    )
