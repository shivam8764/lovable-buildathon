from typing import Dict, Any
from fastapi import HTTPException
from app.db.mongo import get_db
from app.models.schemas import ProgressUpdate

COLL = "user_progress"

async def get_user_progress(user_id: str) -> Dict[str, Any]:
    db = await get_db()
    doc = await db[COLL].find_one({"user_id": user_id}, {"_id": 0})
    return doc or {"user_id": user_id, "progress": [], "summary_vector": {}}

async def update_progress(user_id: str, payload: ProgressUpdate) -> Dict[str, Any]:
    db = await get_db()
    entry = payload.model_dump()
    # upsert entry in array
    res = await db[COLL].update_one(
        {"user_id": user_id, "progress.concept_name": payload.concept_name},
        {"$set": {
            "progress.$.mastery_score": payload.mastery_score,
            "progress.$.time_spent": payload.time_spent,
            "progress.$.attempts": payload.attempts,
            "progress.$.correct": payload.correct,
            "progress.$.status": payload.status,
            "updated_at": __import__("datetime").datetime.utcnow()
        }}
    )
    if res.matched_count == 0:
        await db[COLL].update_one(
            {"user_id": user_id},
            {"$push": {"progress": entry}, "$setOnInsert": {"summary_vector": {}}},
            upsert=True
        )
    # also mirror in summary_vector
    await db[COLL].update_one({"user_id": user_id},
        {"$set": {f"summary_vector.{payload.concept_name}": payload.mastery_score}})
    doc = await db[COLL].find_one({"user_id": user_id}, {"_id": 0})
    return doc
