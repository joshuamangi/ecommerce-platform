import jwt
import datetime

SECRET = "super-secret-key"
ALGORITHM = "HS256"


# encode
def generate_token(user_id: str, role: str):
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


# decode
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"


token = generate_token(user_id="user123", role="admin")
print(f"Token is {token}")
decoded = decode_token(token)
print(f"User is {decoded}")
