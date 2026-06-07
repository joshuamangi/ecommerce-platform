from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from services.common.security.jwt import TokenService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = TokenService.decode_token(token)
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
