FROM python:3.10-slim

WORKDIR /app

# Requirements (backend klasöründe)
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Tüm projeyi kopyala
COPY . .

# FastAPI app çalıştır
CMD ["uvicorn", "backend.fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
