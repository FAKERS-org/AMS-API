from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IDMixin, TimestampMixin


class Department(IDMixin, TimestampMixin, Base):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    students = relationship("Student", back_populates="department")
    faculty = relationship("Faculty", back_populates="department")
    courses = relationship("Course", back_populates="department")
