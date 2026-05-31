from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    id: str
    type: str
    title: str
    description: str = ""
    required: bool = False
    order: int = 0
    config: dict = Field(default_factory=dict)
    validation: dict = Field(default_factory=dict)


class SurveyCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    settings: dict = Field(default_factory=dict)
    questions: list[QuestionBase] = Field(default_factory=list)


class SurveyUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    settings: dict | None = None
    questions: list[QuestionBase] | None = None


class SurveyStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(draft|published|closed)$")


class SurveyOut(BaseModel):
    id: str
    title: str
    description: str
    status: str
    settings: dict
    questions: list[dict]
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None = None

    class Config:
        from_attributes = True


class SurveyListItem(BaseModel):
    id: str
    title: str
    description: str
    status: str
    question_count: int = 0
    response_count: int = 0
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None = None

    class Config:
        from_attributes = True
