from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Genel ortam
    env: str = Field(default="dev", description="Environment: dev | prod")

    # Eski .env değişkenlerini de tanımlayalım
    app_env: str | None = Field(default=None)
    debug: bool = Field(default=False)
    sentiment_provider: str = Field(default="local")
    log_level: str = Field(default="info")
    max_input_length: int = Field(default=500)
    min_input_length: int = Field(default=5)

    # rate limit ayarları
    rate_limit: int = Field(default=10, description="Requests per window")
    rate_limit_window: int = Field(default=60, description="Window in seconds")

    # CORS
    cors_origins: List[str] = Field(
        default=["*"], description="Allowed CORS origins"
    )

    # Model ve data yolları
    sentiment_model_name: str = Field(
        default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    songs_path: str = Field(default="data/songs.json")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
