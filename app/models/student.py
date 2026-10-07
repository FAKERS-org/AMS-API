from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, IDMixin


class Student(IDMixin, TimestampMixin, Base):
    __tablename__ = "students"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    student_id_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    date_of_birth: Mapped[Date | None] = mapped_column(Date, nullable=True)
    department_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id"), nullable=True
    )
    year_level: Mapped[int] = mapped_column(default=1)

    user = relationship("User", back_populates="student_profile")
    department = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")
