# STEM AI Backend (FastAPI + MongoDB)

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# update .env with your Mongo URI/DB

# Seed sample concepts
python seed.py

# Run API
uvicorn app.main:app --reload --port 8000
```

## Key Endpoints
- `GET /health`
- `POST /concepts` (upsert concept)
- `GET /concepts?limit=200`
- `GET /concepts/{name}`
- `GET /concepts/search?q=fractions`
- `GET /concepts/subgraph?topic=Fractions&depth=2`
- `GET /users/{user_id}/progress`
- `POST /users/{user_id}/progress` (body: ProgressUpdate)
- `GET /users/{user_id}/pace`
- `GET /adaptive/map?user_id=u123&topic=Ratios&depth=2`

## Notes
- Uses Motor (async) for MongoDB.
- Adaptive map overlays user mastery and suggests next nodes.
- `algebra_concepts_with_weights.json` is a small seed; swap with your full JSON later.
