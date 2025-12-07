from jose import jwt
from datetime import datetime, timedelta
from bfastapi.app.core.config import settings


def generate_password_reset_token(email: str) -> str:
    expires = datetime.utcnow() + timedelta(hours=1)

    to_encode = {
        "exp": expires,
        "email": email
    }

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded.get("email")
    except Exception:
        return None
