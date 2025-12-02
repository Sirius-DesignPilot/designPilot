from typing import Any, Dict

from fastapi import APIRouter

from app.config import settings


router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """Simple health check endpoint."""

    return {"app_name": settings.APP_NAME, "status": "ok"}
