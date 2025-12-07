from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime



class AnalysisBase(BaseModel):
    title: Optional[str] = None
    input_text: Optional[str] = None
    data_input_type: Optional[str] = "text"   # text, file, url


class AnalysisCreate(AnalysisBase):
    geometry: Optional[Dict[str, Any]] = None   
    errors: Optional[List[str]] = None          
    ai_comment: Optional[str] = None            



class Analysis(BaseModel):
    id: int
    user_id: int

    title: Optional[str]
    input_text: Optional[str]
    data_input_type: Optional[str]

    geometry: Optional[Dict[str, Any]]
    errors: Optional[List[str]]
    ai_comment: Optional[str]

    result: Optional[str] = None  

    created_at: datetime

    class Config:
        from_attributes = True



class AnalysisRequest(BaseModel):
    text: str
    model: Optional[str] ="llama-3.3-70b-versatile"


class AnalysisResult(BaseModel):
    result: str
    confidence: Optional[float] = None
