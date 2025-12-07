from typing import Any
from fastapi import APIRouter
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

# Doğru importlar (senin proje yapına göre)
from  bfastapi.app.api.deps import CurrentUser, SessionDep
from  bfastapi.app.models.analysis import Analysis

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(
    session: SessionDep,
    current_user: CurrentUser
) -> Any:

    # Kullanıcının toplam analiz sayısı
    count_query = (
        select(func.count())
        .select_from(Analysis)
        .where(Analysis.user_id == current_user.id)
    )
    count_result = await session.execute(count_query)
    total_analyses = count_result.scalar_one()

    # Son analiz
    last_analysis_query = (
        select(Analysis)
        .where(Analysis.user_id == current_user.id)
        .order_by(desc(Analysis.id))
        .limit(1)
    )
    last_analysis_result = await session.execute(last_analysis_query)
    last_analysis = last_analysis_result.scalars().first()

    return {
        "username": current_user.email,
        "total_analyses": total_analyses,
        "last_analysis_title": last_analysis.title if last_analysis else "no analysis yet",
        "last_analysis_date": last_analysis.created_at if last_analysis else None,
    }
