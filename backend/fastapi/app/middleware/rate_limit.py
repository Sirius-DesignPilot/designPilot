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

from starlette.exceptions import HTTPException

from .wrappers import Limit

class RateLimitExceeded(HTTPException):

    limit=None

    def __init__(self,limit:Limit)->None:
        self.limit=limit
        if limit.error_message:
            description:str=(
                limit.error_message
                if not callable(limit.error_message)
                else limit.error_message()

            )
        else:
            description=str(limit.limit)
        super(RateLimitExceeded,self).__init__(status_code=429,detail=description)