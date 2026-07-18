from pydantic_settings import BaseSettings, SettingsConfigDict
import os

ENV_FILE = os.getenv("ENV_FILE", ".env.local")


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB: str
    DB_HOST: str
    DB_PORT: int
    REDIS_HOST: str
    REDIS_PORT: int
    CHAOS_ENABLED: bool = False
    CHAOSE_MODE: str = "off"
    CHAOS_PROBABILITY: float = 0.2
    CHAOS_MAX_DELAY: int = 5

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8"
    )

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.POSTGRES_DB}"
        )


settings = Settings()
