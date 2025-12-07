"""import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

limiter=Limiter(
    key_func=get_remote_address,
    default_limits=[os.getenv("DEFAULT_RATE_LIMIT","100/minute")],
    strategy="fixed-window",
    storage_uri="memory://"
)"""

from fastapi import HTTPException


class RateLimitExceeded(HTTPException):

    def __init__(self, limit=None) -> None:
        # limit kullanılmıyorsa opsiyonel bırakılır
        message = str(limit) if limit else "Rate limit exceeded"
        super().__init__(status_code=429, detail=message)
