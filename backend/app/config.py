from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/litesurvey.db"
    upload_dir: str = "./uploads"
    max_upload_size_mb: int = 10
    cors_origins: str = "http://localhost:5173,http://localhost:3000,http://localhost"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def upload_path(self) -> Path:
        p = Path(self.upload_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p

    class Config:
        env_file = ".env"


settings = Settings()
