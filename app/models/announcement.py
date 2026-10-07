from sqlalchemy import String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, IDMixin


class Announcement(IDMixin, TimestampMixin, Base):
    __tablename__ = "announcements"

    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_published: Mapped[bool] = mapped_column(default=False)
    is_pinned: Mapped[bool] = mapped_column(default=False)
