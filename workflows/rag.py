import time
from typing import Dict, Any, List

class RagWorkflow:
    def __init__(self, embedder, store, k: int = 2):
        """
            embedder: EmbeddingService-like object with .embed(text) -> 
        List[float] store: DocumentStore-like object with upsert/search
        """
        self.embedder = embedder
        self.store = store
        self.k = k
        
    def retrieve(self, question: str)-> List[str]:
        emb = self.embedder.embed(question)
        results = self.store.search(emb, limit=self.k)
        return results
    
    def answer(self, context: List[str])-> str:
        if context:
        # preserve original behavior: take first item and truncate to 100 chars
            snippet = context[0]
            display = snippet[:100] + ("..." if len(snippet) > 100 else "")
            return f"I found this: '{display}'"
        return "Sorry, I don't know."
    
    def run(self, question: str)-> Dict[str, Any]:
        start = time.time()
        ctx = self.retrieve(question)
        ans = self.answer(ctx)
        latency = round(time.time()- start, 3)
        return {"question": question, "answer": ans, "context": ctx,
        "latency": latency}