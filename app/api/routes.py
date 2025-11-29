# import library
from fastapi import APIRouter, Depends, HTTPException
from ..models.schemas import QuestionRequest, DocumentRequest, AskResponse, AddResponse, StatusResponse
from ..services.embedding import EmbeddingService
from ..services.store import build_default_store
from ..workflows.rag import RagWorkflow
from typing import Callable

# create FastAPI router
router = APIRouter()

# size of vector embedding dimensions
EMBED_DIM = 128
embedder = EmbeddingService(dim=EMBED_DIM)
store = build_default_store(dim=EMBED_DIM)
workflow = RagWorkflow(embedder=embedder, store=store)

# endpoint to add document
@router.post("/add", response_model=AddResponse)
def add_document(req: DocumentRequest):
    try:
        vec = embedder.embed(req.text)
        doc_id = store.upsert(req.text, vec)
        return {"id": str(doc_id), "status": "added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# endpoint to ask question
@router.post("/ask", response_model=AskResponse)
def ask_question(req: QuestionRequest):
    try:
        res = workflow.run(req.question)
        return {
        "question": res["question"],
        "answer": res["answer"],
        "context_used": res.get("context", []),
        "latency_sec": res.get("latency", 0.0),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# endpoint to check status
@router.get("/status", response_model=StatusResponse)
def status():
    return {
        "qdrant_ready": True if type(store).__name__ == "QdrantStore" else
    False,
        "in_memory_docs_count": store.count(),
        "graph_ready": True,
    }