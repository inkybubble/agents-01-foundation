'''The index saves chunks and their embeddings. When we search, it finds the most similar chunks using cosine similarity

    ┌─────────────────────────────────────────────┐
    │              Retrieval Pipeline             │
    ├─────────────────────────────────────────────┤
    │ Document → Chunker → Embedder → VectorIndex │
    │                                      ↓      │
    │  Query → Embedder → Search → Top-K chunks   │
    └─────────────────────────────────────────────┘

'''

# %%
# Imports
import numpy as np
from typing import List, Tuple
from .embedder import Embedder
from .chunker import chunk_text

# %%
# Vector Index class

class VectorIndex:
    """A basic vector index using numpy"""
    def __init__(self, embedder: Embedder):
        self.embedder=embedder
        self.chunks:List[str]=[]
        self.embeddings: np.ndarray=None

    def add_document(self, text: str)-> None:
        """
        Add a document to the index (chunks it automatically).
        # 1. Chunk the text using chunk_text()
        # 2. Embed all chunks
        # 3. Add to self.chunks and self.embeddings
        """
        new_chunks=chunk_text(text)

        self.chunks.extend(new_chunks)
        new_embeddings=self.embedder.embed(new_chunks)
        if self.embeddings is None or len(self.chunks)==0:
            self.embeddings=new_embeddings
        else:
            self.embeddings=np.vstack([self.embeddings, new_embeddings])

    def search(self, query: str, top_k: int=3,
               min_score: float=0.3) -> List[Tuple[str, float]]:
        """
        Search for similar chunks.
        We're here:
            Query → Embedder → Search → Top-K chunks

        Args:
            query: Search query
            top_k: Number of results to return

          Returns:
            List of (chunk, similarity_score) tuples
        """       
        # similarity = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)) (for a single one)
        # For multiple:
        if self.embeddings is None or len(self.chunks)==0:
            return []
        else:
            query_embedding=self.embedder.embed_single(query)
            similarities = np.dot(self.embeddings, query_embedding) / (np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding))
            top_k_actual=min(top_k, len(similarities))
            idx_sorted_top_k=np.flip(np.argsort(similarities)[-top_k_actual:])
            found=[]
            for idx in idx_sorted_top_k:
                if similarities[idx]>=min_score:
                    found.append((self.chunks[idx], similarities[idx]))
            return found
        