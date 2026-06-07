
from fastapi import Depends, HTTPException, status

from services.common.security.auth import get_current_user


def require_permission(permission: str):

    def checker(current_user=Depends(get_current_user)):
        permissions = current_user.get(
            "permissions", []
        )
        if permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )
        return current_user
    return checker
