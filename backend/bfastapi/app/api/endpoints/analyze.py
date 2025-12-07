
from typing import Any, List
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

# Doğru dependency importları
from bfastapi.app.api.deps import CurrentUser, SessionDep


# Doğru schema importu
from bfastapi.app.schemas import analysis as schemas

# Doğru model importu (senin dizinine göre)
from bfastapi.app.models.analysis import Analysis

# Doğru servis importları
from bfastapi.app.services.analysis_service import AnalysisService
from bfastapi.app.services.ai_service import AIService

router = APIRouter()

analysis_service = AnalysisService()
ai_service = AIService()


@router.post("/list", response_model=List[schemas.Analysis])
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


@router.post("/", response_model=schemas.Analysis)
async def create_analysis(
    session: SessionDep, 
    current_user: CurrentUser,
    analysis_in: schemas.AnalysisCreate
) -> Any:
    new_analysis = await analysis_service.create_analysis(
        session=session,
        current_user=current_user,
        analysis_in=analysis_in
    )
    return new_analysis


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
