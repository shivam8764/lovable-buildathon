from fastapi import APIRouter
from app.models.schemas import ProgressUpdate
from app.services.progress_service import get_user_progress, update_progress
from app.services.pace_service import analyze_pace

router = APIRouter(prefix="/users", tags=["progress"])

@router.get("/{user_id}/progress")
async def read_progress(user_id: str):
    return await get_user_progress(user_id)

@router.post("/{user_id}/progress")
async def write_progress(user_id: str, payload: ProgressUpdate):
    return await update_progress(user_id, payload)

@router.get("/{user_id}/pace")
async def pace(user_id: str):
    return await analyze_pace(user_id)
