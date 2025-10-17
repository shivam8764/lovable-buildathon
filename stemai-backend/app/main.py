from fastapi import FastAPI
from app.routes import concepts, progress, adaptive
from app.services.concept_service import ensure_indexes

app = FastAPI(title="STEM AI Backend (MongoDB)")

app.include_router(concepts.router)
app.include_router(progress.router)
app.include_router(adaptive.router)

@app.on_event("startup")
async def on_startup():
    ensure_indexes()

@app.get("/health")
async def health():
    return {"ok": True}
