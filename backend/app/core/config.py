from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolves to RAGFlow/backend regardless of the process's current working
# directory, so relative paths (.env, uploads) behave the same whether
# uvicorn/alembic/pytest are launched from RAGFlow/ or RAGFlow/backend/.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENV: str = "development"
    APP_NAME: str = "RAGFlow API"
    API_V1_PREFIX: str = "/api/v1"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str

    UPLOAD_DIR: str = "data/uploads"
    MAX_UPLOAD_SIZE_MB: int = 25
    ALLOWED_FILE_TYPES: str = "pdf,png,jpg,jpeg,wav,mp3,m4a,csv,xlsx,xls,docx,txt"

    CORS_ORIGINS: str = "http://localhost:5173"

    @property
    def allowed_file_types_list(self) -> list[str]:
        return [ext.strip().lower() for ext in self.ALLOWED_FILE_TYPES.split(",") if ext.strip()]

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def max_upload_size_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    @property
    def upload_dir_path(self) -> Path:
        path = Path(self.UPLOAD_DIR)
        if not path.is_absolute():
            path = BASE_DIR / path
        path.mkdir(parents=True, exist_ok=True)
        return path


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()