import uuid
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.response import UploadedFile
from app.models.survey import generate_uuid
from app.utils.pagination import success_response

router = APIRouter(prefix="/uploads", tags=["uploads"])

ALLOWED_TYPES = {
    "image/jpeg", "image/png", "image/gif", "image/webp",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/plain", "text/csv",
}


@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    survey_id: str | None = None,
    db: Session = Depends(get_db),
):
    if file.content_type and file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="不支持的文件类型")

    content = await file.read()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=400, detail=f"文件大小不能超过{settings.max_upload_size_mb}MB")

    file_id = generate_uuid()
    ext = Path(file.filename).suffix if file.filename else ""
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
