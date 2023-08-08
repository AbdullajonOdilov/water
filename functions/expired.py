from datetime import datetime
from jose import jwt


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def token_has_expired(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expiration_time = datetime.fromtimestamp(payload.get("exp"))
        current_time = datetime.utcnow()
        return current_time > expiration_time
    except jwt.JWTError:
        return False