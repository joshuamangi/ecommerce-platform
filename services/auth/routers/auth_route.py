import structlog
from data.database import get_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from handlers.auth_handler import AuthService
from schema.auth_schema import LoginRequest, TokenResponse, UserCreate, UserOut

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("Registering User")
    return AuthService.register(db=db, user=user)


@router.post("/login", response_model=TokenResponse)
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    logger.info("User Logging in")
    return AuthService.login(db=db, login_request=credentials)
