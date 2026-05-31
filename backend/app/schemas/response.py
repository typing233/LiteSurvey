from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class ResponseSubmit(BaseModel):
    answers: dict[str, Any] = Field(default_factory=dict)


class ResponseOut(BaseModel):
    id: str
    survey_id: str
    answers: dict[str, Any]
    metadata_: dict = Field(alias="metadata_")
    submitted_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class ResponseListItem(BaseModel):
    id: str
    survey_id: str
    submitted_at: datetime
    metadata_: dict = Field(alias="metadata_")

    class Config:
        from_attributes = True
        populate_by_name = True


class SurveyStats(BaseModel):
    total_responses: int = 0
    today_responses: int = 0
    average_duration: float | None = None
