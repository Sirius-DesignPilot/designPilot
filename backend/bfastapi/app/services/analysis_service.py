from typing import Optional, List
from sqlalchemy import select

from bfastapi.app.api.deps import SessionDep
from bfastapi.app.models.analysis import Analysis
from bfastapi.app.models.user import User
from bfastapi.app.schemas.analysis import AnalysisCreate

# Kullanıcının analizlerini listeleme işlemi
class AnalysisService:
    async def list_analyses(
        self,
        session: SessionDep,
        current_user: User,
        skip: int,
        limit: int
    ):
        # tüm analizleri seç
        stmt = select(Analysis)

        # sadece kullanıcının kendi analizlerini filtrele
        if not current_user.is_superuser:
            stmt = stmt.where(Analysis.user_id == current_user.id)

        # sayfalama için atlama ve limit ekle
        stmt = stmt.offset(skip).limit(limit)

        # sorguyu çalıştır
        result = await session.execute(stmt)

        # analizleri döndür
        return result.scalars().all()

    # Tek analiz getirme işlemi
    async def get_analysis(
        self,
        session: SessionDep,
        current_user: User,
        analysis_id: int
    ):
        stmt = select(Analysis).where(Analysis.id == analysis_id)
        result = await session.execute(stmt)
        analysis = result.scalars().first()

        if not analysis:
            return None

        # izin kontrolü
        if not current_user.is_superuser and analysis.user_id != current_user.id:
            return "not_allowed"

        return analysis

    # Yeni analiz oluşturma işlemi
    async def create_analysis(
        self,
        session: SessionDep,
        current_user: User,
        analysis_in: AnalysisCreate
    ):
        data = analysis_in.model_dump()
        new_analysis = Analysis(**data, user_id=current_user.id)

        session.add(new_analysis)
        await session.commit()
        await session.refresh(new_analysis)

        return new_analysis

    # Analiz silme işlemi
    async def delete_analysis(
        self,
        session: SessionDep,
        current_user: User,
        analysis_id: int
    ):
        stmt = select(Analysis).where(Analysis.id == analysis_id)
        result = await session.execute(stmt)
        analysis = result.scalars().first()

        if not analysis:
            return None

        if not current_user.is_superuser and analysis.user_id != current_user.id:
            return "not_allowed"

        await session.delete(analysis)
        await session.commit()

        return True
