from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Path("./data").mkdir(parents=True, exist_ok=True)
    settings.upload_path  # ensure upload dir exists
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="LiteSurvey API",
    description="轻问 - 轻量级问卷调查平台",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")
