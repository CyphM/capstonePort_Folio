from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str
    user_id: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

class DataOwnerResponse(BaseModel):
    owner: str
    areas: List[str]
    systems: List[str]
    status: str