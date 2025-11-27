# DocumentStore abstraction + Qdrant and InMemory implementations
from abc import ABC, abstractmethod
from typing import List, Optional
import uuid

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import PointStruct, VectorParams, Distance
    _QDRANT_AVAILABLE = True
except Exception:
    _QDRANT_AVAILABLE = False
    
class DocumentStore(ABC):
    @abstractmethod
    def upsert(self, text: str, vector: List[float], doc_id: Optional[str] =
    None)-> str:
        raise NotImplementedError
    
    @abstractmethod
    def search(self, vector: List[float], limit: int = 2)-> List[str]:
        raise NotImplementedError
    
    @abstractmethod
    def count(self)-> int:
        raise NotImplementedError
    
class InMemoryStore(DocumentStore):
    def __init__(self):
        self._docs = [] # list of tuples (id, text)
    def upsert(self, text: str, vector: List[float], doc_id: Optional[str] =
        None)-> str:
        _id = doc_id or str(len(self._docs))
        self._docs.append((_id, text))
        return _id
    def search(self, vector: List[float], limit: int = 2)-> List[str]:
        # naive substring fallback: return docs that contain any token from vector-derived heuristic
        # keep behaviour similar to original demo: check substring of text using an simple heuristic
        # but we will simply return first `limit` docs if present to preserve behaviour
        results = [t for (_id, t) in self._docs if t]
        return results[:limit]
    
    def count(self)-> int:
        return len(self._docs)
    
class QdrantStore(DocumentStore):
    def __init__(self, url: str = "http://localhost:6333", collection_name: str = "demo_collection", dim: int = 128):
        if not _QDRANT_AVAILABLE:
            raise RuntimeError("qdrant-client is not available")
            self.client = QdrantClient(url)
            self.collection = collection_name
            # Create collection if not exists. Do NOT delete existing data in production.
        try:
            # Create if not exists: try to get collection info first.
            self.client.get_collection(collection_name)
        except Exception:
            # create if missing
            self.client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=dim,
                distance=Distance.COSINE),
            )
            
    def upsert(self, text: str, vector: List[float], doc_id: Optional[str] = None)-> str:
        _id = doc_id or str(uuid.uuid4())
        payload = {"text": text}
        point = PointStruct(id=_id, vector=vector, payload=payload)
        self.client.upsert(collection_name=self.collection, points=[point])
        return _id
    
    def search(self, vector: List[float], limit: int = 2)-> List[str]:
        hits = self.client.search(collection_name=self.collection,
        query_vector=vector, limit=limit)
        return [h.payload.get("text") for h in hits if h.payload]
    
    def count(self)-> int:
        try:
            info = self.client.get_collection(self.collection)
            return info.points_count if hasattr(info, "points_count") else 0
        except Exception:
            return 0
 
    def build_default_store(dim: int = 128):
        """Factory: prefer Qdrant if available and running, else in-memory."""
        if _QDRANT_AVAILABLE:
            try:
                return QdrantStore(dim=dim)
            except Exception:
                return InMemoryStore()
        else:
            return InMemoryStore()