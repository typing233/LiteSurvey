from fastapi import APIRouter

from app.api.surveys import router as surveys_router
from app.api.responses import router as responses_router
from app.api.uploads import router as uploads_router

api_router = APIRouter()
api_router.include_router(surveys_router)
api_router.include_router(responses_router)
api_router.include_router(uploads_router)
