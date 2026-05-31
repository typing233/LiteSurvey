from typing import Any, TypeVar, Generic
from pydantic import BaseModel
from sqlalchemy.orm import Session, Query


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Any = None
    pagination: PaginationMeta | None = None


def paginate(query, page: int = 1, page_size: int = 20) -> tuple[list, PaginationMeta]:
    page = max(1, page)
    page_size = min(max(1, page_size), 100)

    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    meta = PaginationMeta(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )
    return items, meta


def success_response(data: Any = None, pagination: PaginationMeta | None = None) -> dict:
    resp = {"code": 0, "message": "success", "data": data}
    if pagination:
        resp["pagination"] = pagination.model_dump()
    return resp


def error_response(code: int, message: str, detail: Any = None) -> dict:
    return {"code": code, "message": message, "detail": detail}
