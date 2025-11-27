from pydantic import BaseModel
from typing import Optional


class AnalysisRequest(BaseModel):
    text: str
    model: Optional[str] = "gpt-4o-mini"


class AnalysisResult(BaseModel):
    result: str
    confidence: Optional[float] = None