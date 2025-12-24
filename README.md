DesignPilot – AI Destekli CAD Çizim Asistanı

DesignPilot, mimari ve teknik CAD çizimlerini analiz eden, hataları tespit eden, AutoCAD komutlarıyla çözüm önerileri sunan ve çizim adımları üretebilen FastAPI + Next.js tabanlı akıllı CAD asistanıdır.

🚀 Özellikler

✔ DXF tabanlı CAD dosya analizi
✔ Geometri ve katman hata tespiti
✔ AutoCAD komut önerileri (_JOIN, _FILLET, _AUDIT, _OVERKILL vb.)
✔ Görsel bazlı çizim analizi (image upload)
✔ Akıllı chat arayüzü
✔ Kullanıcı girişi ve token yapısı
✔ Docker destekli çalıştırma

🏗️ Mimari
designPilot
 ├── backend (FastAPI, AI Service, Rule Engine)
 ├── frontend/auth-ui (Next.js Chat + Login UI)
 ├── docker-compose.yml
 ├── README.md


Backend → FastAPI + AI + Rule Engine

Frontend → Next.js + modern chat UI

AI Engine → Groq Llama 3.3

DB → PostgreSQL (opsiyonel)

⚙️ Kurulum
🔧 1️⃣ Gereksinimler

Docker

Python 3.10+

Node.js 18+

Groq API Key

🐳 Docker ile Çalıştırma (Önerilen)

📌 Proje kökünden:

docker compose up --build


Sonra:

Backend Docs → http://localhost:8000/docs

Frontend UI → http://localhost:3000
 (veya 3001)

🧪 Local Geliştirme (İsteyenler İçin)
Backend
cd backend
pip install -r requirements.txt
uvicorn bfastapi.app.main:app --reload


Backend açılınca:
👉 http://127.0.0.1:8000/docs

Frontend (Auth + Chat UI)
cd frontend/auth-ui
npm install
npm run dev


👉 http://localhost:3000

🔐 Ortam Değişkenleri

backend/.env.example örneğini .env yapın:

GROQ_API_KEY=your_groq_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/designpilot


⚠ .env GitHub’a gönderilmez, sadece localde saklanır.

🧠 Kullanım

Chat ekranından komut yaz:

“Bu CAD çizimindeki hataları analiz et”

“18.5 cm çaplı dişli çark için teknik çizim adımları oluştur”

DXF / PNG / JPG yükleyerek analiz al

AI teknik hata raporu döner:

Hata açıklaması

Nedenler

Çözüm

AutoCAD komutları

🛠️ Teknolojiler

FastAPI

Next.js

Groq AI

PostgreSQL

Docker

ezDXF / CAD Processing

📌 Notlar

DWG desteklenmez → DXF’e dönüştürüp yükleyin

Vision analizi PNG/JPG destekler

Rule Engine gelişmeye açıktır

🤝 Katkı

PR açabilirsiniz 🎉
Branch yapısı:

main → stabil
dev → geliştirme
feature/* → özellik geliştirme

👤 Geliştiren

DesignPilot AI Team
