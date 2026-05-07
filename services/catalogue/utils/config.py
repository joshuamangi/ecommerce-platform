import platform
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}"
            f"@localhost:5432/"
            f"{self.POSTGRES_DB}"
        )

    class Config:
        """Fetching the location of the env file"""
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
