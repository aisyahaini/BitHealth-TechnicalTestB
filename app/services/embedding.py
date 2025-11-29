# import library
import hashlib
import random
from typing import List

# EembeddingService: encapsulate embedding logic (fake/deterministic for demo)
class EmbeddingService:
    def __init__(self, dim: int = 128):
        self.dim = dim
        
    def _stable_seed(self, text: str)-> int:
        h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return int(h, 16) % (2**32)
    
    def embed(self, text: str)-> List[float]:
        """
        Produce a deterministic pseudo-embedding for the given text.
        For a production system replace this with a call to a real embedding 
        model.
        """
        seed = self._stable_seed(text)
        rnd = random.Random(seed)
        return [rnd.random() for _ in range(self.dim)]