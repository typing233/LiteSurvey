from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.survey import Survey
from app.models.response import Response
from app.schemas.response import ResponseSubmit, SurveyStats
from app.services.response_service import validate_response
from app.utils.pagination import paginate, success_response

router = APIRouter(tags=["responses"])


@router.get("/public/surveys/{survey_id}")
def get_public_survey(survey_id: str, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey or survey.status != "published":
        raise HTTPException(status_code=404, detail="问卷不存在或未发布")
    return success_response({
        "id": survey.id,
        "title": survey.title,
        "description": survey.description,
        "questions": survey.questions,
        "settings": survey.settings,
    })


@router.post("/public/surveys/{survey_id}/responses")
def submit_response(survey_id: str, body: ResponseSubmit, request: Request, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey or survey.status != "published":
        raise HTTPException(status_code=404, detail="问卷不存在或未发布")

    errors = validate_response(survey.questions or [], body.answers)
    if errors:
        raise HTTPException(status_code=422, detail={"errors": errors})

    response = Response(
        survey_id=survey_id,
        answers=body.answers,
        metadata_={
            "ip": request.client.host if request.client else "",
            "user_agent": request.headers.get("user-agent", ""),
        },
    )
    db.add(response)
    db.commit()
    return success_response({"id": response.id})


@router.get("/surveys/{survey_id}/responses")
def list_responses(
    survey_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Response).filter(Response.survey_id == survey_id).order_by(Response.submitted_at.desc())
    items, meta = paginate(query, page, page_size)
    data = []
    for r in items:
        data.append({
            "id": r.id,
            "survey_id": r.survey_id,
            "answers": r.answers,
            "metadata": r.metadata_,
            "submitted_at": r.submitted_at.isoformat() if r.submitted_at else None,
        })
    return success_response(data, meta)


@router.get("/surveys/{survey_id}/responses/{response_id}")
def get_response(survey_id: str, response_id: str, db: Session = Depends(get_db)):
    resp = db.query(Response).filter(
        Response.id == response_id, Response.survey_id == survey_id
    ).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Response not found")
    return success_response({
        "id": resp.id,
        "survey_id": resp.survey_id,
        "answers": resp.answers,
        "metadata": resp.metadata_,
        "submitted_at": resp.submitted_at.isoformat() if resp.submitted_at else None,
    })


@router.delete("/surveys/{survey_id}/responses/{response_id}")
def delete_response(survey_id: str, response_id: str, db: Session = Depends(get_db)):
    resp = db.query(Response).filter(
        Response.id == response_id, Response.survey_id == survey_id
    ).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Response not found")
    db.delete(resp)
    db.commit()
    return success_response(None)


@router.get("/surveys/{survey_id}/stats")
def get_stats(survey_id: str, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    total = db.query(func.count(Response.id)).filter(Response.survey_id == survey_id).scalar() or 0

    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today = db.query(func.count(Response.id)).filter(
        Response.survey_id == survey_id,
        Response.submitted_at >= today_start,
    ).scalar() or 0

    return success_response({
        "total_responses": total,
        "today_responses": today,
    })
