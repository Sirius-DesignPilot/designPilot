
from typing import Any,List
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
#zaten async session veriyor from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import CurrentUser, SessionDep
from app.schemas import analysis as schemas
from app.api.deps import CurrentUser, SessionDep
from app.models.analysis import Analysis
from app.services.analysis_service import AnalysisService
from app.services.ai_service import AIService

router = APIRouter()

analysis_service = AnalysisService()
ai_service = AIService()


@router.get("/", response_model=List[schemas.Analysis])
async def read_analyses(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100
) -> Any:
    analyses = await analysis_service.list_analyses(
        session=session,
        current_user=current_user,
        skip=skip,
        limit=limit
    )
    return analyses


"""
@router.get("/",response_model=List[schemas.Analysis])
async def read_analyses(
        session:SessionDep,
        current_user:CurrentUser,
        skip:int=0,
        limit:int=100
)->Any:
   
    kullanıcının analizlerini listeler
    :param session:
    :param current_user:
    :param skip:
    :param limit:
    :return:
  
    stmt=select(Analysis)

    if not current_user.is_superuser:
        stmt=stmt.where(Analysis.user_id==current_user.id)

    stmt=stmt.offset(skip).limit(limit)

    result=await session.execute(stmt)
    analyses=result.scalars().all()

    return analyses
"""

@router.get("/{id}", response_model=schemas.Analysis)
async def read_analysis(
    id: int,
    session: SessionDep,
    current_user: CurrentUser
) -> Any:
    analysis = await analysis_service.get_analysis(
        session=session,
        current_user=current_user,
        analysis_id=id
    )

    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if analysis == "not_allowed":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return analysis

"""
@router.get("/{id}",response_model=schemas.Analysis)
async def read_analysis(
        id:int,
        session:SessionDep,
        current_user:CurrentUser,
)->Any:
  
    Id'ye göre analiz detayını getir.
    :param id:
    :param session:
    :param current_user:
    :return:
    
    result=await session.execute(select(Analysis).where(Analysis.id==id))
    analysis=result.scalars().first()

    if not analysis:
        raise HTTPException(status_code=404,detail="Analysis not found")

    if not current_user.is_superuser and (analysis.user_id !=current_user.id):
        raise HTTPException(status_code=40,detail="not enough permissions")

    return analysis
"""
@router.post("/", response_model=schemas.Analysis)
async def create_analysis(
    session: SessionDep, # type: ignore
    current_user: CurrentUser,
    analysis_in: schemas.AnalysisCreate
) -> Any:
    new_analysis = await analysis_service.create_analysis(
        session=session,
        current_user=current_user,
        analysis_in=analysis_in
    )
    return new_analysis

"""
@router.post("/",response_model=schemas.Analysis)
def create_analysis(
        *,
        session:SessionDep,
        current_user:CurrentUser,
        analysis_in:schemas.AnalysisCreate
)->Any:
   
    create a new analysis
    :param session:
    :param current_user:
    :param analysis_in:
    :return:
  
    analysis_data=analysis_in.model_dump()
    new_analysis=Analysis(**analysis_data,user_id=current_user.id)

    session.add(new_analysis)
    session.commit()
    session.refresh(new_analysis)
    return new_analysis
"""

@router.delete("/{id}")
async def delete_analysis(
    id: int,
    session: SessionDep,
    current_user: CurrentUser
) -> Any:
    result = await analysis_service.delete_analysis(
        session=session,
        current_user=current_user,
        analysis_id=id
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if result == "not_allowed":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return {"Message": "Analysis deleted"}

"""
@router.delete("/{id}")
async def delete_analysis(
        session:SessionDep,current_user:CurrentUser,id:int
)->Any:
  
    delete an analysis
    :param session: 
    :param current_user: 
    :param id: 
    :return: 
   
    result=await session.execute(select(Analysis).where(Analysis.id==id))
    analysis=result.scalars().first()

    if not analysis:
        raise HTTPException(status_code=404,detail="Analysis not found")
    if not current_user.is_superuser and (analysis.user_id !=current_user.id):
        raise HTTPException(status_code=40,detail="not enough permissions")
    await session.delete(analysis)
    await session.commit()
    return {"Message":"Analysis deleted"}
"""