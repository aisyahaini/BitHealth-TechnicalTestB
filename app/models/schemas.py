from pydantic import BaseModel
from typing import List

class QuestionRequest(BaseModel):
    question: str
 
class DocumentRequest(BaseModel):
    text: str
 
class AskResponse(BaseModel):
    question: str
    answer: str
    context_used: List[str]
    latency_sec: float
 
class AddResponse(BaseModel):
    id: str
    status: str
 
class StatusResponse(BaseModel):
    qdrant_ready: bool
    in_memory_docs_count: int
    graph_ready: bool