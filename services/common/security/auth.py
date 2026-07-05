import jwt
import structlog

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from services.common.security.jwt import TokenService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

logger = structlog.get_logger(__name__)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = TokenService.decode_token(token)

        if not isinstance(payload, dict):
            logger.exception("Invalid token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        logger.info("User Authorized")
        return payload

    except jwt.ExpiredSignatureError:
        logger.exception("Token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )

    except jwt.InvalidTokenError:
        logger.exception("Invalid token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
