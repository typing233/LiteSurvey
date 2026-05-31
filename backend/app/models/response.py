from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, JSON, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.survey import generate_uuid, utcnow


class Response(Base):
    __tablename__ = "responses"
    __table_args__ = (
        Index("ix_responses_survey_id", "survey_id"),
        Index("ix_responses_submitted_at", "submitted_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    survey_id: Mapped[str] = mapped_column(String(36), nullable=False)
    answers: Mapped[dict] = mapped_column(JSON, default=dict)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    survey_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    original_name: Mapped[str] = mapped_column(Text, nullable=False)
    stored_path: Mapped[str] = mapped_column(Text, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), default="")
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
