from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IDMixin, TimestampMixin


class Enrollment(IDMixin, TimestampMixin, Base):
    __tablename__ = "enrollments"

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), index=True
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), index=True
    )

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
