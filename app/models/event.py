import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum as SAEnum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, IDMixin, TimestampMixin


class EventCategory(str, enum.Enum):
    NEWS = "news"
    EVENTS = "events"


class Event(IDMixin, TimestampMixin, Base):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[EventCategory] = mapped_column(
        SAEnum(EventCategory), default=EventCategory.EVENTS, index=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    preview: Mapped[str | None] = mapped_column(String(500), nullable=True)
    published_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tag: Mapped[str | None] = mapped_column(String(100), nullable=True)
    photo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    event_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    published_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status: Mapped[str] = mapped_column(String(50), default="active")
    is_published: Mapped[bool] = mapped_column(default=True)

