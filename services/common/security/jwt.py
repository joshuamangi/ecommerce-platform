import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"


class TokenService:

    # encode
    @staticmethod
    def create_access_token(data: dict):
        payload = data.copy()
        payload["exp"] = (datetime.utcnow() + timedelta(minutes=30)
                          )
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # decode
    @staticmethod
    def decode_token(token: str):
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
