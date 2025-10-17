from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class EdgeRef(BaseModel):
    topic: str
    weight: float = Field(0.7, ge=0.0, le=1.0)

class ConceptIn(BaseModel):
    name: str
    domain: str = "Mathematics"
    grade_level: Optional[int] = None
    description: Optional[str] = None
    tags: List[str] = []
    depends_on: List[EdgeRef] = []
    leads_to: List[EdgeRef] = []

class ConceptOut(ConceptIn):
    id: Optional[str] = None

class DependencyIn(BaseModel):
    source: str
    target: str
    weight: float = Field(0.7, ge=0.0, le=1.0)

class ProgressEntry(BaseModel):
    concept_name: str
    mastery_score: float = Field(0.0, ge=0.0, le=1.0)
    time_spent: int = 0
    attempts: int = 0
    correct: int = 0
    status: str = "learning"  # learning / review / weak / mastered

class ProgressDoc(BaseModel):
    user_id: str
    grade_level: Optional[int] = None
    progress: List[ProgressEntry] = []
    summary_vector: Dict[str, float] = {}

class ProgressUpdate(BaseModel):
    concept_name: str
    mastery_score: float = Field(0.0, ge=0.0, le=1.0)
    time_spent: int = 0
    attempts: int = 0
    correct: int = 0
    status: str = "learning"

class SubgraphRequest(BaseModel):
    topic: str
    depth: int = Field(2, ge=1, le=5)

class AdaptiveMapRequest(BaseModel):
    user_id: str
    topic: str
    depth: int = Field(2, ge=1, le=5)
