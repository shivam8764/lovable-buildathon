from fastapi import APIRouter
from app.models.schemas import AdaptiveMapRequest
from app.services.adaptive_service import adaptive_map

router = APIRouter(prefix="/adaptive", tags=["adaptive"])

@router.get("/map")
async def get_adaptive_map(user_id: str, topic: str, depth: int = 2):
    return await adaptive_map(user_id, topic, depth)
