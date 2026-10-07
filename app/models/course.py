from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, IDMixin


class Course(IDMixin, TimestampMixin, Base):
    __tablename__ = "courses"

    code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    credit_hours: Mapped[int] = mapped_column(Integer, default=3)
    department_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id"), nullable=True
    )
    is_published: Mapped[bool] = mapped_column(default=False)

    department = relationship("Department", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    
    faculty_assignments = relationship(
        "CourseFaculty",
        back_populates="course",
        cascade="all, delete-orphan",
    )
