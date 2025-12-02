# designPilot
MVP for yazanZeka

## Backend API (FastAPI)

The backend now exposes an AI analysis endpoint that proxies requests to the configured OpenAI model (or returns a deterministic echo response when no API key is provided).

- Run locally:
  ```bash
  cd backend/fastapi
  uvicorn app.main:app --reload --app-dir .
  ```

- Default endpoints:
  - `GET /api/v1/health/` — simple health check
  - `POST /api/v1/analyze/` — send `{ "text": "..." }` and receive the AI result

Configure your OpenAI key by setting `OPENAI_API_KEY` in a `.env` file next to `backend/fastapi/app/config.py`.

## Frontend (Next.js)

The frontend includes an `/analysis` page that posts text to the backend API and renders the AI response. Set `NEXT_PUBLIC_API_BASE_URL` in the frontend environment (defaults to `http://localhost:8000`).
