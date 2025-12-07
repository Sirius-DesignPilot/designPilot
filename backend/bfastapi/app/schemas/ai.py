from pydantic import BaseModel
from typing import Optional, List, Literal

class EvaluationRequest(BaseModel):
    steps: List[str]
    image_base64: Optional[str] = None
    language: Optional[Literal["tr", "en"]] = "tr"

class StepEval(BaseModel):
    step_index: int
    status: Literal["correct", "partial", "missing", "wrong"]
    comment: str

class EvaluationResponse(BaseModel):
    steps: List[StepEval]
    overall_score: float
    note: Optional[str] = None

class GenerationRequest(BaseModel):
    prompt: str
    language: Optional[Literal["tr", "en"]] = "tr"

class GenerationResponse(BaseModel):
    title: str
    steps: List[str]
