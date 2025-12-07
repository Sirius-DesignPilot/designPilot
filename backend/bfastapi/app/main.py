import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------------------------------
# 1) FASTAPI instance ilk sırada oluşturulmalı
# -----------------------------------------------------
app = FastAPI(
    title="DesignPilot API",
    version="1.0.0",
)

# -----------------------------------------------------
# 2) CORS MIDDLEWARE — FastAPI oluşturulduktan hemen sonra
# -----------------------------------------------------
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # burada liste kullanılıyor
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------
# 3) .env yükleme
# -----------------------------------------------------
ENV_PATH = r"C:\designP\designPilot\backend\.env"
load_dotenv(ENV_PATH)

print("API KEY:", os.getenv("GROQ_API_KEY"))

# -----------------------------------------------------
# 4) ARTIK diğer modüller import edilebilir
# -----------------------------------------------------
from .core.config import settings
from .database import engine, Base

from .api.endpoints import analyze, auth, dashboard, health

from ai.service import AIService
from bfastapi.app.schemas.ai import (
    EvaluationRequest,
    EvaluationResponse,
    GenerationRequest,
    GenerationResponse
)

# AI servisi örneği
ai_service = AIService()


# -----------------------------------------------------
# 5) AI API ENDPOINTLERİ
# -----------------------------------------------------
@app.post("/api/v1/ai/evaluate", response_model=EvaluationResponse)
async def evaluate_drawing_api(req: EvaluationRequest):
    return await ai_service.evaluate_drawing(req)


@app.post("/api/v1/ai/generate", response_model=GenerationResponse)
async def generate_api(req: GenerationRequest):
    return await ai_service.generate_steps(req)


# -----------------------------------------------------
# 6) ANALYSIS ENDPOINTİ
# -----------------------------------------------------
@app.post("/api/v1/analysis", response_model=GenerationResponse)
async def create_new_analysis(req: GenerationRequest):
    try:
        return await ai_service.generate_steps(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Adım üretme hatası: {e}")


# -----------------------------------------------------
# 7) ROUTER EKLEME (CORS’TAN SONRA!)
# -----------------------------------------------------
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Auth"])
app.include_router(analyze.router, prefix=settings.API_V1_STR + "/analyses", tags=["Analyze"])
app.include_router(dashboard.router, prefix=settings.API_V1_STR, tags=["Dashboard"])


# -----------------------------------------------------
# 8) STARTUP EVENT
# -----------------------------------------------------
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("PostgreSQL bağlantısı kuruldu.")
    print("AI Agent servisi başlatıldı.")


# -----------------------------------------------------
# 9) ROOT ENDPOINT
# -----------------------------------------------------
@app.get("/")
def root():
    return {"message": "DesignPilot API is running!"}
