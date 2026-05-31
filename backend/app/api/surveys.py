import copy
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.survey import Survey, generate_uuid, utcnow
from app.models.response import Response
from app.schemas.survey import (
    SurveyCreate, SurveyUpdate, SurveyStatusUpdate, SurveyOut, SurveyListItem,
)
from app.utils.pagination import paginate, success_response, error_response

router = APIRouter(prefix="/surveys", tags=["surveys"])


@router.get("")
def list_surveys(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Survey).order_by(Survey.created_at.desc())
    if status:
        query = query.filter(Survey.status == status)

    items, meta = paginate(query, page, page_size)

    survey_ids = [s.id for s in items]
    response_counts = {}
    if survey_ids:
        counts = (
            db.query(Response.survey_id, func.count(Response.id))
            .filter(Response.survey_id.in_(survey_ids))
            .group_by(Response.survey_id)
            .all()
        )
        response_counts = dict(counts)

    data = []
    for s in items:
        data.append({
            "id": s.id,
            "title": s.title,
            "description": s.description,
            "status": s.status,
            "question_count": len(s.questions) if s.questions else 0,
            "response_count": response_counts.get(s.id, 0),
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "updated_at": s.updated_at.isoformat() if s.updated_at else None,
            "published_at": s.published_at.isoformat() if s.published_at else None,
        })

    return success_response(data, meta)


@router.post("")
def create_survey(body: SurveyCreate, db: Session = Depends(get_db)):
    survey = Survey(
        id=generate_uuid(),
        title=body.title,
        description=body.description,
        settings=body.settings,
        questions=[q.model_dump() for q in body.questions],
    )
    db.add(survey)
    db.commit()
    db.refresh(survey)
    return success_response(SurveyOut.model_validate(survey).model_dump())


@router.get("/{survey_id}")
def get_survey(survey_id: str, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return success_response(SurveyOut.model_validate(survey).model_dump())


@router.put("/{survey_id}")
def update_survey(survey_id: str, body: SurveyUpdate, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    if body.title is not None:
        survey.title = body.title
    if body.description is not None:
        survey.description = body.description
    if body.settings is not None:
        survey.settings = body.settings
    if body.questions is not None:
        survey.questions = [q.model_dump() for q in body.questions]

    survey.updated_at = utcnow()
    db.commit()
    db.refresh(survey)
    return success_response(SurveyOut.model_validate(survey).model_dump())


@router.delete("/{survey_id}")
def delete_survey(survey_id: str, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    db.query(Response).filter(Response.survey_id == survey_id).delete()
    db.delete(survey)
    db.commit()
    return success_response(None)


@router.patch("/{survey_id}/status")
def update_status(survey_id: str, body: SurveyStatusUpdate, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    survey.status = body.status
    if body.status == "published" and not survey.published_at:
        survey.published_at = utcnow()
    survey.updated_at = utcnow()
    db.commit()
    db.refresh(survey)
    return success_response(SurveyOut.model_validate(survey).model_dump())


@router.post("/{survey_id}/duplicate")
def duplicate_survey(survey_id: str, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    new_survey = Survey(
        id=generate_uuid(),
        title=f"{survey.title} (副本)",
        description=survey.description,
        settings=copy.deepcopy(survey.settings) if survey.settings else {},
        questions=copy.deepcopy(survey.questions) if survey.questions else [],
        status="draft",
    )
    db.add(new_survey)
    db.commit()
    db.refresh(new_survey)
    return success_response(SurveyOut.model_validate(new_survey).model_dump())
