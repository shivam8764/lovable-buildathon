from typing import List, Dict, Any
from app.db.mongo import get_db
from app.models.schemas import ConceptIn
from fastapi import HTTPException

CONCEPTS = "concepts"

def ensure_indexes():
    db = get_db()
    db[CONCEPTS].create_index("name", unique=True)
    db[CONCEPTS].create_index("domain")
    db[CONCEPTS].create_index("depends_on.topic")
    db[CONCEPTS].create_index("leads_to.topic")

def upsert_concept(payload: ConceptIn) -> Dict[str, Any]:
    db =  get_db()
    doc = payload.model_dump()
    doc["updated_at"] = __import__("datetime").datetime.utcnow()
    db[CONCEPTS].update_one({"name": payload.name}, {"$set": doc}, upsert=True)
    return doc

def get_concept(name: str) -> Dict[str, Any]:
    db =  get_db()
    doc =  db[CONCEPTS].find_one({"name": name})
    if not doc:
        raise HTTPException(404, "Concept not found")
    doc["id"] = str(doc.pop("_id"))
    return doc

def list_concepts(limit: int = 200) -> List[Dict[str, Any]]:
    print("Inside list_concepts")
    db =  get_db()
    cursor = db[CONCEPTS].find({}, {"_id": 0}).limit(limit)
    return [doc for doc in cursor]

def search_concepts(q: str, limit: int = 50) -> List[Dict[str, Any]]:
    db =  get_db()
    cursor = db[CONCEPTS].find({
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"tags": {"$regex": q, "$options": "i"}}
        ]
    }, {"_id": 0}).limit(limit)
    return [doc for doc in cursor]

def get_subgraph(topic: str, depth: int = 2) -> Dict[str, Any]:
    db =  get_db()
    center =  db[CONCEPTS].find_one({"name": topic}, {"_id": 0})
    if not center:
        raise HTTPException(404, "Topic not found")

    # BFS outward by leads_to and inward by depends_on up to depth
    seen = {topic}
    frontier = [topic]
    nodes = {topic: center}
    edges = []

    for _ in range(depth):
        next_frontier = []
        for t in frontier:
            # outward
            for doc in db[CONCEPTS].find({"depends_on.topic": t}, {"_id": 0}):
                name = doc["name"]
                if name not in seen:
                    seen.add(name); nodes[name] = doc; next_frontier.append(name)
                # find weight from t->name
                w = next((e["weight"] for e in doc.get("depends_on", []) if e["topic"] == t), 0.7)
                edges.append({"source": t, "target": name, "weight": w})
            # inward
            src =  db[CONCEPTS].find_one({"name": t}, {"_id": 0})
            for lead in src.get("leads_to", []):
                name = lead["topic"]
                doc =  db[CONCEPTS].find_one({"name": name}, {"_id": 0})
                if doc:
                    if name not in seen:
                        seen.add(name); nodes[name] = doc; next_frontier.append(name)
                    edges.append({"source": t, "target": name, "weight": lead.get("weight", 0.7)})
        frontier = next_frontier

    return {
        "center": topic,
        "nodes": list(nodes.values()),
        "edges": edges
    }
