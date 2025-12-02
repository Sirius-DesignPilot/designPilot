from fastapi import APIRouter, HTTPException

from app.schemas.analysis import AnalysisRequest, AnalysisResult
from app.services.ai_service import AIService


router = APIRouter()
ai_service = AIService()


@router.post("/", response_model=AnalysisResult)
async def analyze_text(payload: AnalysisRequest) -> AnalysisResult:
    """Run the AI text analysis pipeline.

    The endpoint sends the provided text to the configured AI model and
    returns the structured result. A clear 502 is raised when the upstream
    model fails so the frontend can surface a meaningful error.
    """

    result = await ai_service.get_prediction(
        input_data={"text": payload.text},
        model=payload.model,
    )

    if "error" in result:
        raise HTTPException(status_code=502, detail=result["error"])

    return AnalysisResult(**result)
