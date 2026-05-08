from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from utils.config import settings

DATABASE_URL = settings.DATABASE_URL


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Yields the db Session for dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
