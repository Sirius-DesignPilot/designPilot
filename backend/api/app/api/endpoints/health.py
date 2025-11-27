from fastapi import APIRouter, Depends,HTTPException,status
from typing import Any,Dict
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import SessionDep
from app.config import settings

router=APIRouter()

@router.get("/",response_model=Dict[str,Any])
async def health_check(
        session:SessionDep
)->Any:
    """
    health check
    :param session:
    :return:
    """
    health_status={
        "app_name":settings.APP_NAME,
        "status":"ok",
        "database":"unknown",
    }

    try:
        await session.execute(text("SELECT 1"))
        health_status["database"]="connected"

    except Exception as e:
        health_status["status"]="error"
        health_status["database"]="disconnected"
        health_status["detail"]=str(e)

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_status
        )