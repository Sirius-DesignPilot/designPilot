import base64
import re
import os
import json
from typing import Optional, List, Literal, Any

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

        self.model = "llama-3.3-70b-versatile"

    # ------------------------------------------------------------------
    # 1) CAD DOSYA ANALİZİ (DXF/DWG)  → teknik rapor + kural motoru
    # ------------------------------------------------------------------
    async def analyze_file(self, file: UploadFile) -> dict:
        """
        DXF/DWG dosyasını parse eder, rule engine ile hataları bulur
        ve AI'dan teknik analiz raporu üretir.
        """
        # 1. Geometriyi oku
        geometry = self.dwg_parser.parse(file)

        # 2. Kurallara göre hataları bul
        errors = self.rules.evaluate(geometry)

        # 3. Teknik analiz promptunu hazırla
        prompt = self._ai_analysis_prompt(geometry, errors)

        # 4. Groq'a gönder
        ai_response = self._call_groq(prompt)

        return {
            "ai_analysis": ai_response,
            "errors": errors,
            "geometry": geometry,
        }

    def _ai_analysis_prompt(self, geometry: Any, errors: Any) -> str:
        """
        Kural motoru + geometri verisini kullanarak modeli
        sadece teknik analiz yapmaya zorlayan prompt.
        """
        return f"""
Sen kıdemli bir Mimari CAD Denetim Uzmanısın.
SADECE aşağıdaki verileri kullanarak teknik rapor yazacaksın:

- CAD geometry verisi
- Rule Engine hataları

❌ ASLA YAPMAYACAKSIN:
- Kullanıcıya eğitim vermek
- “kontrol edin, inceleyin, bakın, çizimi açın” gibi genel ifadeler
- Tahmine dayalı hata üretmek
- Veri dışı yorum yapmak

EĞER HİÇ HATA YOKSA:
"Hiç hata bulunamadı. Çizim teknik standartlara uygundur." yaz.
Başka hiçbir şey ekleme.

---

[CAD GEOMETRİ VERİSİ]
{json.dumps(geometry, indent=2, ensure_ascii=False)}

[TEKNİK HATA KAYITLARI]
{json.dumps(errors, indent=2, ensure_ascii=False)}

---

YANIT FORMATIN KESİNLİKLE BU OLACAK:

### 🛠 Teknik Hata Analizi
Her hata şu formatta olmalı:
- ID: (Rule Engine id)
- Tür: geometry | layer | dimension | naming
- Eleman: entity id
- Açıklama: kısa ama net teknik açıklama

### 🚀 Düzeltme Reçetesi
Her hata için:
- **Hata:** kısa başlık
- **AutoCAD Çözümü:** (örn: _JOIN, _FILLET, _AUDIT, -LAYER SET …)
- **Uygulama Adımları:** teknik işlem sırası

### 💡 Profesyonel Öneriler
(en fazla 3 madde, sadece teknik)
"""

    def _call_groq(self, prompt: str) -> str:
        """
        Metin tabanlı teknik analiz için Groq LLM çağrısı.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a STRICT CAD technical inspection AI. "
                            "You ONLY talk about technical issues explicitly shown in the provided data. "
                            "You NEVER give generic training instructions like 'open the drawing, check layers'. "
                            "You NEVER guess missing information. "
                            "If there are no errors, you say exactly: "
                            "\"Hiç hata bulunamadı. Çizim teknik standartlara uygundur.\""
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.15,
                max_tokens=3500,
            )

            return completion.choices[0].message.content
        except Exception as e:
            return f"Groq API Error: {str(e)}"

    # ------------------------------------------------------------------
    # 2) ADIM ÜRETME (metin prompt → JSON steps)
    # ------------------------------------------------------------------
    
    async def generate_steps(self, req: GenerationRequest) -> GenerationResponse:
      print("🟦 AIService.generate_steps ÇAĞRILDI")
      print("🟦 Prompt:", req.prompt)

      text = req.prompt.lower()

    # 🔹 Hata / analiz odaklı mı, yoksa normal çizim isteği mi?
      hata_anahtar_kelimeler = ["hata", "analiz", "hatalarını", "hatalarini", "hata analizi"]

      if any(kw in text for kw in hata_anahtar_kelimeler):
        # HATA ANALİZ MODU
        system_prompt = self.build_error_analysis_prompt(req.prompt, req.language or "tr")
      else:
        # NORMAL ÇİZİM ADIMI MODU
        system_prompt = self.build_generation_prompt(req.prompt, req.language or "tr")

      messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Lütfen JSON formatında yanıtla: {req.prompt}"},
      ]

      try:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
      except Exception as e:
        raise RuntimeError(f"Model çağrısı hatası: {e}")

      raw = completion.choices[0].message.content.strip()
      cleaned = self._clean_json(raw)
      parsed = json.loads(cleaned)

      return GenerationResponse(
        title=parsed.get("title", req.prompt),
        steps=parsed.get("steps", []),
      )


    async def evaluate_drawing(self, req: EvaluationRequest) -> EvaluationResponse:
        system_prompt = self._build_evaluation_prompt(req.steps, req.language)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Sadece geçerli JSON formatında cevap ver."},
        ]

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        raw = completion.choices[0].message.content.strip()
        cleaned = self._clean_json(raw)
        parsed = json.loads(cleaned)

        return EvaluationResponse(
            steps=parsed.get("steps", []),
            overall_score=parsed.get("overall_score", 0.0),
            note=parsed.get("note"),
        )

    def generate_autocad_script(self, ai_analysis: str) -> str:
        """
        AI analizinden AutoCAD komutlarını ayıklar ve .scr içeriği oluşturur.
        """
        script_commands: List[str] = []

        upper = ai_analysis.upper()
        if "OVERKILL" in upper:
            script_commands.append("_OVERKILL _ALL  _Accept")
        if "PURGE" in upper:
            script_commands.append("-PURGE _All * _No")
        if "REGEN" in upper:
            script_commands.append("_REGEN")

        return "\n".join(script_commands)

    # ------------------------------------------------------------------
    # 3) RULE ENGINE + ANALİZ → AutoCAD FIX SCRIPT
    # ------------------------------------------------------------------
    def generate_fix_script(self, ai_analysis: str, errors: List[dict]) -> str:
        """
        AI raporunu ve kural motoru hatalarını tarayarak bir .scr dosyası içeriği oluşturur.
        errors: CADRuleEngine'den gelen structured hata listesi (dict).
        """
        script: List[str] = []
        script.append("(princ \"\\nAI Otomatik Düzeltme Basliyor...\\n\")")

        # 1️⃣ Genel temizlik komutları (AI analizine göre)
        upper = ai_analysis.upper()
        if "OVERKILL" in upper:
            script.append("_OVERKILL ALL  ")
        if "PURGE" in upper:
            script.append("-PURGE ALL * N")
        if "AUDIT" in upper or "HATA" in upper:
            script.append("_AUDIT Y")

        # 2️⃣ Spesifik hatalara göre işlem
        for err in errors:
            # GEOMETRİ – kapanmayan polyline
            if (
                err.get("type") == "geometry"
                and "Polyline is not closed" in err.get("description", "")
            ):
                script.append(f"SELECT {err.get('entity')} _JOIN")

            # LAYER HATASI
            if err.get("type") == "layer":
                expected = err.get("expected_layer", "A-WALL")
                script.append(f"-LAYER SET {expected}")
                script.append(
                    f"CHANGE {err.get('entity')} PROPERTIES LAYER {expected}"
                )

            # ÖRNEK: özel ID'li bir geometri hatası
            if err.get("id") == "G003":
                script.append("_FILLET R 0")
                script.append(f"SELECT {err.get('entity')}")

        script.append("_REGEN")
        script.append("(princ \"\\nDüzeltmeler Tamamlandi.\\n\")")

        return "\n".join(script)

    # ------------------------------------------------------------------
    # 4) GENERATION / EVALUATION PROMPT YARDIMCI METODLARI
    # ------------------------------------------------------------------
    

    def build_generation_prompt(self, prompt: str, language: str = "tr") -> str:
     """
    Normal çizim isteği için (örn. '18.5 cm çapında dişli çark çiz')
    adım adım ÇİZİM TALİMATI üretir.
    """
     return f"""
Sen profesyonel bir mimari / teknik çizim ve CAD asistanısın.
Görevin: Kullanıcının çizim isteğini, AutoCAD'de uygulanabilir NET ADIMLARA dönüştürmek.

❗ ÇOK ÖNEMLİ:
- SADECE geçerli JSON döndür.
- JSON dışında **tek bir kelime bile** yazma.
- "title" mutlaka doldur (ör: "18.5 cm Çaplı Dişli Çark Çizimi").
- "steps" mutlaka DOLU bir liste olsun.
- Her adım, AutoCAD komut/adımları içeren uygulanabilir bir talimat olsun.

ÖRNEK ADIM YAPISI:
- "1. AutoCAD'de yeni bir çizim aç, units'i cm olarak ayarla."
- "2. _CIRCLE komutunu kullanarak merkezde 18.5 cm çapında daire çiz."
- "3. Diş profilini oluşturmak için ..."

FORMAT:
{{
  "title": "çizimin kısa açıklaması",
  "steps": [
    "1. ...",
    "2. ...",
    "3. ..."
  ]
}}

KULLANICI İSTEĞİ:
{prompt}
"""



    def build_error_analysis_prompt(self, prompt: str, language: str = "tr") -> str:
     """
    'bu cad çizimindeki hataları analiz et' gibi istekler için,
    Hata | Olası neden | Çözüm formatında liste üretir.
    """
     return f"""
Sen profesyonel bir mimari çizim ve CAD HATA ANALİZİ asistanısın.

KULLANICI senden metin tabanlı olarak bir çizimin veya çalışmanın
OLASI HATALARINI ve ÇÖZÜMLERİNİ isteyecek.

Görevin:
- "Hata: ... | Olası neden: ... | Çözüm: ..." formatında maddeler üretmek.
- Çözüm kısmında imkân oldukça AutoCAD komutları (_MOVE, _SCALE, _ARRAYPOLAR, _OVERKILL, _AUDIT, _XREF, _BIND, _STYLE vb.) kullanmak.

❌ KESİNLİKLE YAPMAYACAKLARIN:
- "Çizimi açın, katmanları kontrol edin, zoom yapın" gibi genel prosedür yazmak.
- Kullanıcıya CAD dersi verir gibi uzun, soyut tavsiyeler yazmak.
- Çok genel, herkese uyan cümleler üretmek.

✅ YAPACAKLARIN:
- 5–10 arası net HATA & ÇÖZÜM maddesi üret.
- Her maddede:
  - Hata türü
  - Olası teknik sebep
  - AutoCAD odaklı çözüm adımları olsun.

SADECE geçerli JSON döndür.

FORMAT:
{{
  "title": "analizin başlığı (ör: 'Muhtemel CAD Hata Analizi')",
  "steps": [
    "Hata: ... | Olası neden: ... | Çözüm: ...",
    "Hata: ... | Olası neden: ... | Çözüm: ...",
    "..."
  ]
}}

KULLANICI İSTEĞİ:
{prompt}
"""


    def _build_evaluation_prompt(
        self, steps: List[str], language: str = "tr"
    ) -> str:
        return f"""
Sen bir CAD eğitim değerlendirme asistanısın.
Kullanıcıya verilen adımları değerlendirip, her adım için durum ve yorum döneceksin.

SADECE geçerli JSON döndür.

FORMAT:
{{
  "steps": [
    {{"step_index": 0, "status": "correct", "comment": "Açıklama"}},
    {{"step_index": 1, "status": "partial", "comment": "Açıklama"}}
  ],
  "overall_score": 85.0,
  "note": "Genel değerlendirme notu"
}}

DEĞERLENDİRİLECEK ADIMLAR:
{json.dumps(steps, ensure_ascii=False, indent=2)}
"""

    def _clean_json(self, text: str) -> str:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1].strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

        # Kontrol karakterlerini temizle
        cleaned = re.sub(r"[\x00-\x1f]", "", cleaned, flags=re.UNICODE)
        return cleaned

    # ------------------------------------------------------------------
    # 5) GÖRSEL ANALİZ (PNG/JPG → vision modeli)
    # ------------------------------------------------------------------
    async def analyze_image_visual(self, file: UploadFile) -> str:
        """
        Resim dosyalarını (PNG, JPEG) vision modeliyle analiz eder.
        """
        try:
            content = await file.read()
            encoded_image = base64.b64encode(content).decode("utf-8")

            prompt = """
Sen bir Mimari Proje Denetçisisin.
Bu görseldeki çizimi teknik olarak incele.
SADECE şunları listele:
1. Görseldeki teknik hatalar (ölçek, yerleşim, sembol hataları).
2. Mimari standartlara aykırı durumlar.
3. Çözüm önerileri.
Format: ### ❌ Teknik Hata Listesi ... ### 🚀 Çözüm Önerileri ...
"""

            return await self._call_vision_model(prompt, encoded_image)
        except Exception as e:
            return f"Görsel analiz hatası: {str(e)}"

    async def _call_vision_model(self, prompt: str, image_base64: str) -> str:
        """
        Vision destekli modeli çağırmak için basit bir örnek stub.
        Burayı kullandığın Groq vision modeline göre özelleştirebilirsin.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a CAD vision inspection AI.",
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                },
                            },
                        ],
                    },
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Groq Vision API Error: {str(e)}"
