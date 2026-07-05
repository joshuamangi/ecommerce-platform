import datetime
import structlog
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from data.models import User
from schema.auth_schema import LoginRequest, TokenResponse, UserCreate
from utils.password import PasswordService
from services.common.security.jwt import TokenService

logger = structlog.get_logger(__name__)


class AuthService:

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Fetch a user by email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def register(db: Session, user: UserCreate):
        existing = AuthService.get_user_by_email(db=db, email=user.email)
        if existing:
            logger.exception("Email already in use")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already in use. Please Register using another email"
            )

        hashed = PasswordService.hash_password(user.password)
        new_user = AuthService.create_user(
            db=db, user=user, password_hash=hashed)
        return new_user

    @staticmethod
    def create_user(db: Session, user: UserCreate, password_hash: str) -> User:
        """Create a new User record and return it."""
        new_user = User(
            email=user.email,
            password_hash=password_hash,
            permissions=user.permissions,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info("User created")
        return new_user

    @staticmethod
    def authenticate_user(db: Session, email: str, plain_password: str):
        user = AuthService.get_user_by_email(db=db, email=email)
        if not user:
            logger.warning("User Not Found")
            return None
        if not PasswordService.verify_password(plain_password=plain_password, password_hash=user.password_hash):
            logger.warning("Invalid user/password")
            return None
        return user

    @staticmethod
    def login(db: Session, login_request: LoginRequest):
        user = AuthService.authenticate_user(
            db=db, email=login_request.email, plain_password=login_request.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = TokenService.create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
                "permissions": user.permissions,
            }
        )
        token_repsonse = TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )
        return token_repsonse
