from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IDMixin, TimestampMixin


class Award(IDMixin, TimestampMixin, Base):
    __tablename__ = "awards"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    achievement: Mapped[str | None] = mapped_column(String(255), nullable=True)
    imagepath: Mapped[str | None] = mapped_column(String(500), nullable=True)
    recipient_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    student_id: Mapped[int | None] = mapped_column(
        ForeignKey("students.id", ondelete="SET NULL"), nullable=True
    )
    award_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    is_published: Mapped[bool] = mapped_column(default=True)

    student = relationship("Student")

