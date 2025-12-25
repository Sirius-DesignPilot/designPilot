FROM python:3.10-slim

WORKDIR /app

# Requirements (backend klasöründe)
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --default-timeout=200 --retries 5 --no-cache-dir -r requirements.txt


# Tüm projeyi kopyala
COPY . .

# FastAPI app çalıştır
CMD ["uvicorn", "backend.fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
