from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, IDMixin, TimestampMixin


class Project(IDMixin, TimestampMixin, Base):
    __tablename__ = "projects"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    partner: Mapped[str | None] = mapped_column(String(255), nullable=True)
    duration: Mapped[str | None] = mapped_column(String(100), nullable=True)
    funding: Mapped[str | None] = mapped_column(String(100), nullable=True)
    investigators: Mapped[str | None] = mapped_column(String(255), nullable=True)
    students: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ongoing")
    is_published: Mapped[bool] = mapped_column(default=True)

