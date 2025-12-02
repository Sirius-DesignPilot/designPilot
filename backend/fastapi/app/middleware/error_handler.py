from cyclopts import ValidationError
from fastapi import Request,FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi.errors import RateLimitExceeded
import logging

logger=logging.getLogger("uvicorn.error")
def register_exception_handlers(app:FastAPI):

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request:Request,exc:RateLimitExceeded):
        logger.warning(f"Rate limit exceeded:{request.client.host}")
        return JSONResponse(
            status_code=429,
            content={
                "success":False,
                "error":"Rate Limit exceeded",
                "message":f"çok fazla istek gönderildi. Lütfen {exc.limit} sınırına dikkat edin."
            }
        )
    
    @app.add_exception_handler(RequestValidationError)
    async def validation_error(_:Request,
                               exc:Union[RequestValidationError,ValidationError],
                               )->JSONResponse:
        return JSONResponse(
            {"errors":exc.errors()},
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, # type: ignore
        )
    validation_error_response_definition["properties"]={ # type: ignore
        "errors":{
            "success":False,
            "error":"Validation Error",
            "message":"Gönderilen verilerde hata var.",
            "details":formatted_errors, # type: ignore
        }
    }
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": "HTTP Exception",
                "message": exc.detail
            }
        )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Global error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal Server Error",
                "message": "Sunucu tarafında beklenmeyen bir hata oluştu."
            }
        )



        