from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.response import UploadedFile
from app.models.survey import generate_uuid
from app.utils.pagination import success_response

router = APIRouter(prefix="/uploads", tags=["uploads"])

ALLOWED_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".txt", ".csv",
}


@router.get("/config")
def get_upload_config():
    return success_response({
        "max_size_mb": settings.max_upload_size_mb,
        "allowed_extensions": sorted(ALLOWED_EXTENSIONS),
    })


@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    survey_id: str | None = None,
    max_size_mb: int | None = Query(None, description="Per-question size limit from config"),
    db: Session = Depends(get_db),
):
    ext = Path(file.filename).suffix.lower() if file.filename else ""
    if ext and ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {ext}")

    content = await file.read()

    effective_max_mb = min(max_size_mb, settings.max_upload_size_mb) if max_size_mb else settings.max_upload_size_mb
    max_bytes = effective_max_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=400, detail=f"文件大小不能超过{effective_max_mb}MB")

    file_id = generate_uuid()
    stored_name = f"{file_id}{ext}"
    stored_path = settings.upload_path / stored_name

    with open(stored_path, "wb") as f:
        f.write(content)

    record = UploadedFile(
        id=file_id,
        survey_id=survey_id,
        original_name=file.filename or "unnamed",
        stored_path=stored_name,
        mime_type=file.content_type or "",
        size_bytes=len(content),
    )
    db.add(record)
    db.commit()

    return success_response({
        "id": file_id,
        "url": f"/uploads/{stored_name}",
        "original_name": record.original_name,
        "size_bytes": record.size_bytes,
    })
