import logging
from typing import Union

from fastapi import Request, FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from slowapi.errors import RateLimitExceeded # type: ignore
from cyclopts import ValidationError


logger = logging.getLogger("uvicorn.error")


def register_exception_handlers(app: FastAPI):

    
    @bfastapi.bfastapi.app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        logger.warning(f"Rate limit exceeded: {request.client.host}")
        return JSONResponse(
            status_code=429,
            content={
                "success": False,
                "error": "Rate Limit Exceeded",
                "message": f"Çok fazla istek gönderildi. Lütfen limit ({exc.limit}) değerine dikkat edin."
            }
        )

    
    @bfastapi.bfastapi.app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: Union[RequestValidationError, ValidationError]
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": "Validation Error",
                "message": "Gönderilen verilerde hata var.",
                "details": exc.errors(),
            },
        )

    
    @bfastapi.bfastapi.app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": "HTTP Exception",
                "message": exc.detail
            },
        )

    
    @bfastapi.bfastapi.app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Global error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal Server Error",
                "message": "Sunucu tarafında beklenmeyen bir hata oluştu."
            },
        )
