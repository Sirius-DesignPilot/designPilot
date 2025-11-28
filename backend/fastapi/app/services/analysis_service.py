from typing import Optional, List
from sqlalchemy import select

from app.api.deps import SessionDep
from app.models.analysis import Analysis
from app.models.user import User
from app.schemas.analysis import AnalysisCreate

#Kullanıcının analizlerini listeleme işlemi."""
class AnalysisService:
    async def list_analyses(
         self,session:SessionDep,current_user:User,skip:int,limit:int
            ):
        stmt=select(Analysis)#tüm analizleri seç
        if not current_user.is_superuser:
            stmt=stmt.where(Analysis.user_id==current_user.id)#sadece kullanıcının kendi analizlerini filtrele
        stmt=stmt.offset(skip).limit(limit)#sayfalama için atlama ve limit ekle
        result=await session.execute(stmt)#sorguyu çalıştır
        return result.scalars().all()#analizleri döndür

    #Tek Analiz getirme işlemi
    async def get_analysis(
        self, session: SessionDep, current_user: User, analysis_id: int
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
    
    #Yeni analiz oluşturma işlemi
    async def create_analysis(
        self, session: SessionDep, current_user: User, analysis_in: AnalysisCreate
    ):
        data = analysis_in.model_dump()
        new_analysis = Analysis(**data, user_id=current_user.id)

        session.add(new_analysis)
        await session.commit()
        await session.refresh(new_analysis)

        return new_analysis
    
    #Analiz silme işlemi
    async def delete_analysis(
        self, session: SessionDep, current_user: User, analysis_id: int
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
