

import os
import json
from typing import Optional, List, Literal
from fastapi import UploadFile
from groq import Groq
from pydantic import BaseModel
from bfastapi.app.utils.dwg_parser import DWGParser
from bfastapi.app.utils.image_analyzer import ImageAnalyzer
from bfastapi.app.utils.cad_rules import CADRuleEngine

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


class AIService:

    def __init__(self):
        self.dwg_parser = DWGParser()
        self.image_analyzer = ImageAnalyzer()
        self.rules = CADRuleEngine()

        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY ortam değişkeni bulunamadı.")
        self.client = Groq(api_key=api_key)

        
        self.model ="llama-3.3-70b-versatile"  


    async def analyze_file(self, file: UploadFile):
        filename = file.filename.lower()

       
        if filename.endswith((".dwg", ".dxf")):
            geometry = self.dwg_parser.parse(file)
        else:
            geometry = self.image_analyzer.analyze(file)

        
        errors = self.rules.evaluate(geometry)

        
        ai_text = self._ai_analysis_prompt(geometry, errors)
        ai_response = self._call_groq(ai_text)

        return {
            "geometry": geometry,
            "errors": errors,
            "ai_analysis": ai_response
        }

    
    def _ai_analysis_prompt(self, geometry, errors):
        return f"""
You are an expert CAD drawing inspector and AutoCAD expert.

Geometry extracted from drawing:
{json.dumps(geometry, indent=2)}

Detected issues:
{json.dumps(errors, indent=2)}

Provide:
1. Explanation of each error
2. Fix instructions with exact AutoCAD commands
3. Best practices for architectural drafting
4. Suggestions to improve the drawing
"""

   

    print("🟦 MODEL ÇAĞRILIYOR (llama-3.1-70b-versatile)")

    def _call_groq(self, prompt: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional CAD expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=4096,
            )
            return completion.choices[0].message["content"]
        except Exception as e:
            return f"Groq API Error: {str(e)}"

    async def generate_steps(self, req: GenerationRequest) -> GenerationResponse:
        print("🟦 AIService.generate_steps ÇAĞRILDI")
        print("🟦 Prompt:", req.prompt)

        system_prompt = self.build_generation_prompt(req.prompt)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Lütfen JSON formatında yanıtla: {req.prompt}"}
        ]

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
            )
        except Exception as e:
            raise RuntimeError(f"Model çağrısı hatası: {e}")

        raw = completion.choices[0].message.content.strip()
        cleaned = self._clean_json(raw)

        parsed = json.loads(cleaned)
        return GenerationResponse(
            title=parsed.get("title", req.prompt),
            steps=parsed.get("steps", [])
        )

    async def evaluate_drawing(self, req: EvaluationRequest) -> EvaluationResponse:
        system_prompt = self._build_evaluation_prompt(req.steps)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Sadece geçerli JSON formatında cevap ver."}
        ]

        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )

        raw = completion.choices[0].message.content.strip()
        cleaned = self._clean_json(raw)
        parsed = json.loads(cleaned)

        return EvaluationResponse(
            steps=parsed.get("steps", []),
            overall_score=parsed.get("overall_score", 0.0),
            note=parsed.get("note")
        )

    def build_generation_prompt(prompt: str, language="tr"):
        return f"""
Sen profesyonel bir mimari çizim ve CAD asistanısın.
Görevin: Kullanıcının çizim isteğini teknik olarak doğru, adım adım açıklayan bir çizim yönergesi oluşturmaktır.

❗ ÇOK ÖNEMLİ:
- SADECE geçerli JSON döndür.
- JSON dışında **tek bir kelime bile** yazma.
- "title" mutlaka doldur.
- "steps" mutlaka DOLU bir liste olsun (boş liste asla döndürme).
- Adımlar net, uygulanabilir CAD komutları içersin.

FORMAT:
{{
  "title": "çizimin kısa açıklaması",
  "steps": ["Adım 1 ...", "Adım 2 ...", "Adım 3 ..."]
}}

KULLANICI İSTEĞİ:
{prompt}"""


    def _clean_json(self, text: str) -> str:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1].strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
        return cleaned
