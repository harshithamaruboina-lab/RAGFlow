# RAGFlow

Multi-Modal Knowledge Graph Synthesis for Enterprise Compliance.

## Phase 0 — Engineering Foundation

This phase delivers: FastAPI skeleton, PostgreSQL + Alembic migrations, JWT
authentication, and a real (unparsed) document upload pipeline with per-user
isolation. No parsing, embeddings, graph, or RAG logic yet — that begins in
later phases.

## Prerequisites

- Python 3.12 (already set up in `backend/.venv`)
- Docker Desktop (for PostgreSQL)
- Git

## Quickstart (Windows / PowerShell, run from the RAGFlow root)

See the full command sequence provided alongside this README. In short:

```powershell
.\backend\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
pip install -r backend\requirements-dev.txt
Copy-Item backend\.env.example backend\.env   # then edit SECRET_KEY
docker compose up -d db
cd backend; alembic upgrade head; cd ..
cd backend; pytest -v; cd ..
uvicorn app.main:app --reload --app-dir backend --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000/docs

## Project layout