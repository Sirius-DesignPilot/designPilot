from typing import Optional

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    text: str = Field(..., description="User provided text to analyze")
    model: str = Field(default="gpt-4o-mini", description="AI model name")


class AnalysisResult(BaseModel):
    result: str
    confidence: Optional[float] = None
