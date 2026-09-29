# HealthKey Backend

The backend for **HealthKey**, a digital health record system connecting patients, doctors, and hospitals. Built with **Django REST Framework** on a **Supabase (PostgreSQL)** database, with an **AI module** that estimates diabetes risk from patient data.

## Features
- **OTP authentication** by national ID (`/auth/request-otp/`, `/auth/verify-otp/`)
- **Doctor portal**: patient visits, symptoms, diagnoses, lab results, and prescriptions
- **Patient data model**: hospitals, doctors, patients, visits, lab tests, appointments, drugs, emergency info, lifestyle
- **AI diabetes risk prediction**: an XGBoost model combined with features from a medical **knowledge graph** (NetworkX)
- REST APIs consumed by the [HealthKey mobile app](https://github.com/alablaq26-lab/health_app)

## Tech Stack
Python · Django 5 · Django REST Framework · Supabase / PostgreSQL · XGBoost · pandas · NetworkX

## Project Structure
```
projectBackend/
├── api/              # Reports API, Supabase helpers
├── authentication/   # OTP login
├── create_user/      # Doctor portal, patients, visits, prescriptions
└── ai_engine/        # Prediction model, knowledge graph, forms
```

## Getting Started
```bash
git clone https://github.com/alablaq26-lab/HealthKey_1.git
cd HealthKey_1/projectBackend
python -m venv projectVenv && source projectVenv/bin/activate
pip install -r requirements.txt
```
Create a `.env` file (never commit it):
```
user=...
password=...
host=...
port=...
dbname=...
SUPABASE_URL=...
SUPABASE_KEY=...
```
Then:
```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## Related Projects
- [health_app](https://github.com/alablaq26-lab/health_app): patient mobile app (Flutter)
- [medical-ui](https://github.com/alablaq26-lab/medical-ui): doctor visit interface prototype (Next.js)
