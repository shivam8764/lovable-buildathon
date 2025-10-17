from typing import Dict, Any
from app.db.mongo import get_db

LOGS = "activity_logs"
PROG = "user_progress"

async def analyze_pace(user_id: str) -> Dict[str, Any]:
    db = await get_db()
    # simplistic heuristic
    doc = await db[PROG].find_one({"user_id": user_id}, {"_id": 0, "progress": 1})
    progress = doc.get("progress", []) if doc else []
    topics_attempted = len(progress)
    avg_mastery = sum(p.get("mastery_score", 0.0) for p in progress) / topics_attempted if topics_attempted else 0.0

    # last 10 logs duration
    cursor = db[LOGS].find({"user_id": user_id}).sort("timestamp", -1).limit(10)
    durations = [l.get("duration_sec", 0) async for l in cursor]
    avg_duration = sum(durations) / len(durations) if durations else 0

    alert = None
    if topics_attempted >= 5 and avg_mastery < 0.5:
        alert = "⚠️ Foundational mismatch: pace exceeds comprehension. Revisit prerequisites."
    status = "✅ Pace OK" if not alert else alert
    return {"topics_attempted": topics_attempted, "avg_mastery": avg_mastery, "avg_duration_sec": avg_duration, "status": status}
