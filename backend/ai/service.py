
import base64
import re
import os
import json
from typing import Optional, List, Literal
from fastapi import UploadFile
from groq import Groq
from pydantic import BaseModel
from bfastapi.app.utils.dwg_parser import DWGParser
from bfastapi.app.utils.image_analyzer import ImageAnalyzer
from bfastapi.app.utils.cad_rules import CADRuleEngine
from bfastapi.app.utils.dwg_parser import DWGParser
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
    # 1. Geometriyi ezdxf ile oku
       geometry = self.dwg_parser.parse(file) 
    
    # 2. Matematiksel hataları kural motoruyla bul (boşluklar, katmanlar vb.)
       errors = self.rules.evaluate(geometry)

    # 3. AI'ya verileri göndererek teknik rapor oluştur
       ai_text = self._ai_analysis_prompt(geometry, errors)
       ai_response = self._call_groq(ai_text) 

       return {
        "report": ai_response,
        "raw_errors": errors
    }

    
    def _ai_analysis_prompt(self, geometry, errors):
    # Bu metodun en başına JSON kütüphanesini import ettiğinizden emin olun
    
    
     return f"""
Sen profesyonel bir Kıdemli Mimari Denetçi ve AutoCAD uzmanısın. 
Görevin: Genel tavsiye vermek değil, aşağıdaki teknik verileri analiz ederek spesifik hataları listelemektir.

[CAD GEOMETRİ VERİSİ]
{json.dumps(geometry, indent=2)}

[KURAL MOTORU TESPİTLERİ]
{json.dumps(errors, indent=2)}

Lütfen yanıtını ŞU FORMATTA hazırla (Başka açıklama ekleme):

### 🛠 Teknik Hata Analizi
- **Geometrik Hatalar:** (Örn: "0.5 birimden küçük boşluklar: L12 ve L45 uçları birleşmiyor.")
- **Katman Hataları:** (Örn: "A-DOOR katmanında olması gereken bloklar 0 katmanında.")
- **Metin Uyumsuzlukları:** (Örn: "Mekan ismi 'GARAJ' ancak alan hesaplaması 12m2'nin altında.")

### 🚀 Düzeltme Reçetesi (AutoCAD Çözümleri)
- **Hata:** [Spesifik Tanım]
- **Kesin Çözüm:** [AutoCAD Komutu: Örn. _FILLET, _JOIN, _CHSPACE]
- **Uygulama:** [Teknik uygulama adımı]

### 💡 Profesyonel Tavsiyeler
- Çizim performansını artırmak için `OVERKILL` ve `PURGE` önerileri.
"""
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
    

    def generate_autocad_script(self, ai_analysis: str) -> str:
        """
        AI analizinden AutoCAD komutlarını ayıklar ve .scr içeriği oluşturur.
        """
        script_commands = []
        # AI yanıtındaki komutları yakalamak için basit bir regex veya anahtar kelime taraması
        if "OVERKILL" in ai_analysis.upper():
            script_commands.append("_OVERKILL _ALL  _Accept")
        if "PURGE" in ai_analysis.upper():
            script_commands.append("-PURGE _All * _No")
        if "REGEN" in ai_analysis.upper():
            script_commands.append("_REGEN")
            
        return "\n".join(script_commands)
    
    def generate_fix_script(self, ai_analysis: str, errors: List[str]) -> str:
        """
        AI raporunu ve kural motoru hatalarını tarayarak bir .scr dosyası içeriği oluşturur.
        """
        script_commands = ["(princ \"\\nAI Otomatik Düzeltme Baslatiliyor...\\n\")"]
        
        # 1. Genel Temizlik Komutları (Analiz raporuna göre tetiklenir)
        analysis_upper = ai_analysis.upper()
        if "OVERKILL" in analysis_upper:
            script_commands.append("_OVERKILL _ALL  _Accept")
        if "PURGE" in analysis_upper:
            script_commands.append("-PURGE _All * _No")
        if "AUDIT" in analysis_upper or "HATA" in analysis_upper:
            script_commands.append("_AUDIT _Yes")
            
        # 2. Katman Standartlaştırma (Kural motoru çıktılarına göre)
        for error in errors:
            if "Non-standard layer" in error:
                # Örn: "Non-standard layer detected: 0" -> Standart bir katmana taşıma önerisi
                bad_layer = error.split(":")[-1].strip()
                script_commands.append(f"-LAYER _Set A-WALL _Ch {bad_layer}  ")

        script_commands.append("_REGEN")
        script_commands.append("(princ \"\\nDüzeltmeler Tamamlandi.\\n\")")
        
        return "\n".join(script_commands)

    def build_generation_prompt(self,prompt: str, language="tr"):
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

            cleaned = re.sub(r'[\x00-\x1f]', '', cleaned, flags=re.UNICODE)
        
        return cleaned
    

    
    # ai/service.py
    async def analyze_image_visual(self, file: UploadFile):
            """Resim dosyalarını (PNG, JPEG) Vision modeliyle analiz eder."""
            try:
                # Dosyayı oku ve base64 formatına çevir
                content = await file.read()
                encoded_image = base64.b64encode(content).decode('utf-8')

                # Teknik denetçi promptu
                prompt = """
                Sen bir Mimari Proje Denetçisiyim.
                Bu görseldeki çizimi teknik olarak incele.
                SADECE şunları listele:
                1. Görseldeki teknik hatalar (ölçek, yerleşim, sembol hataları).
                2. Mimari standartlara aykırı durumlar.
                3. Çözüm önerileri.
                Format: ### ❌ Teknik Hata Listesi ... ### 🚀 Çözüm Önerileri ...
                """

                # Not: Burada kullandığınız API'nin (Groq Llama-3-Vision vb.)
                # vision metodunu çağırmalısınız.
                return await self._call_vision_model(prompt, encoded_image)
            except Exception as e:
                return f"Görsel analiz hatası: {str(e)}"

    async def analyze_file(self, file: UploadFile):
            """DXF dosyalarını parser üzerinden analiz eder."""
            
            parser = DWGParser()
            rule_engine = CADRuleEngine()

            # Geometri verilerini çıkar
            geometry = parser.parse(file)
            # Kurallara göre hataları bul
            errors = rule_engine.evaluate(geometry)

            # AI'ya teknik rapor hazırlat
            prompt = f"Geometri: {geometry}\nSistem Hataları: {errors}\nBu verileri profesyonel bir rapor haline getir."
            ai_analysis = await self._call_groq(prompt)

            return {
                "ai_analysis": ai_analysis,
                "errors": errors,
                "geometry": geometry
            }

    def generate_fix_script(self, analysis, errors):
            """AutoCAD için LISP/Script üretir."""
            # Basit bir script üretim mantığı
            return "(command \"_AUDIT\" \"Y\")\n(command \"_PURGE\" \"A\" \"*\" \"N\")"