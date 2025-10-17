from fastapi import APIRouter
from app.models.schemas import ConceptIn, SubgraphRequest
from app.services.concept_service import upsert_concept, get_concept, list_concepts, search_concepts, get_subgraph

router = APIRouter(prefix="/concepts", tags=["concepts"])

@router.post("")
def create_or_update_concept(payload: ConceptIn):
    return upsert_concept(payload)

@router.get("/{name}")
def read_concept(name: str):
    return get_concept(name)

@router.get("")
def read_concepts(limit: int = 200):
    return list_concepts(limit)

@router.get("/search")
def search(q: str, limit: int = 50):
    return search_concepts(q, limit)

@router.get("/subgraph")
def subgraph(topic: str, depth: int = 2):
    return get_subgraph(topic, depth)
