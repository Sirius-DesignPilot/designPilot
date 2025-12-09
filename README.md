🧩 DesignPilot AI — Akıllı CAD Çizim Asistanı
AutoCAD / DWG dosyalarını analiz eden, çizim hatalarını tespit eden ve profesyonel çizim yönergeleri oluşturan Yapay Zekâ destekli asistan.
🚀 Proje Özeti

DesignPilot, mimarlar ve mühendisler için geliştirilmiş bir AI destekli CAD çizim asistanıdır.
Sistem, DWG veya görsel formatlı çizimleri analiz eder, yapısal hataları belirler ve kullanıcıya profesyonel çizim adımları önerir.

🎯 Ana Özellikler
🔍 1. DWG / Görsel Çizim Analizi

AutoCAD DWG / DXF dosyaları okunur (DWGParser)

Görsel tabanlı çizimler işlenir (ImageAnalyzer)

Geometri çıkarımı yapılır

Mimari çizim kurallarına göre hata tespiti yapılır (CADRuleEngine)

🤖 2. Yapay Zekâ ile Çizim Yönergeleri Üretimi

Groq'un LLaMA modelleri kullanılarak:

Kullanıcının verdiği prompt’a göre adım adım çizim rehberleri üretilir

JSON formatında temiz çıktı elde edilir

TR / EN dil desteği mevcuttur

✏️ 3. Çizim Değerlendirme

Kullanıcının kendi çizim adımları AI tarafından analiz edilir:

correct

partial

missing

wrong

Değerlendirme, JSON formatında geri döner.

👤 4. Kullanıcı Yönetimi & Yetkilendirme

JWT tabanlı login / signup

Süper kullanıcı ve normal kullanıcı ayrımı

Kullanıcıya özel analiz listeleri

📊 5. Dashboard & Analiz Geçmişi

Kullanıcının tüm analiz geçmişi listelenir

Backend’den filtrelenmiş veri gelir

🧱 6. Modern Frontend

Next.js 14 (App Router)

Modern UI (TailwindCSS)

Chat benzeri etkileşimli assitant ekranı

🏗️ Mimari
designPilot/
│
├── backend/
│   ├── bfastapi/app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── analyze.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── dashboard.py
│   │   │   │   └── health.py
│   │   │   └── deps.py
│   │   ├── ai/
│   │   │   ├── service.py   ← AI beyni
│   │   │   ├── dwg_parser.py
│   │   │   ├── image_analyzer.py
│   │   │   └── cad_rules.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── analysis.py
│   │   ├── schemas/
│   │   │   ├── analysis.py
│   │   │   └── ai.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   └── analysis_service.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   └── database.py
│   └── ai/ (ayrı servis)
│       └── service.py
│
└── frontend/
    └── auth-ui/src/app/
        ├── chat/
        ├── dashboard/
        ├── login/
        ├── signup/
        └── forgot-password/

🧠 AI Servisi Nasıl Çalışıyor?
✨ Kullanılan Model

Varsayılan model:

llama-3.1-70b-versatile (Groq)


GroqClient şu şekilde başlatılır:

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

Çizim Yönergesi Üretimi
completion = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[ ... ]
)


Modelden gelen çıktı JSON parse edilir ve frontend’e döner.

📡 Önemli API Endpointleri
🔵 1) Adım Üretme (AI)
POST /api/v1/ai/generate

Request
{
  "prompt": "yarıçapı 30 olan bir daire çiz",
  "language": "tr"
}

Response
{
  "title": "Daire Çizimi",
  "steps": [
    "Çizim düzlemini aç.",
    "Circle komutunu başlat.",
    "Merkez noktasını belirle.",
    "30 cm yarıçapını gir."
  ]
}

🔵 2) Çizim Değerlendirme
POST /api/v1/ai/evaluate

🔵 3) Analiz Yönetimi
GET /api/v1/analyses/list
POST /api/v1/analyses/
GET /api/v1/analyses/{id}
DELETE /api/v1/analyses/{id}

🗄️ Veritabanı (PostgreSQL)
Kullanılan tablo:
analyses


Alanlar:

id

user_id

title

input_text

data_input_type

result

created_at

Tüm modeller SQLAlchemy ile tanımlıdır.

🛠️ Kurulum
1) Backend
a) Sanal ortam
python -m venv venv
venv\Scripts\activate

b) Gereksinimler
pip install -r requirements.txt

c) .env dosyası oluştur
GROQ_API_KEY=...
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/postgres
SECRET_KEY=...

d) Backend çalıştır
uvicorn bfastapi.app.main:app --reload

2) Frontend
cd frontend/auth-ui
npm install
npm run dev

🔐 Kimlik Doğrulama

JWT tabanlı

Bearer <token> ile istek gönderilir

Token üretimi core/security.py içinde yönetilir

🧪 Test

API testleri için önerilen araç:

Insomnia

Postman

VS Code REST Client

🚧 Geliştirme Yol Haritası
Özellik	Durum

DWG parse	✅ Temel işlevler tamam

Görsel analiz	⚠️ Geliştirilebilir

AI step generation	✅ Çalışıyor

AI evaluation	⚠️ JSON refining iyileştirilebilir

Drawing rule engine	⚠️ Daha fazla mimari kural eklenebilir

Çoklu model desteği	📝 Yol haritasında

Pro planı & kullanıcı limitleme	📝 Eklenebilir
