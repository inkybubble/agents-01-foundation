# %%
# Imports
from sentence_transformers import SentenceTransformer

import numpy as np
from typing import List

# %%
# Embedder class

class Embedder:
    "Generate embeddings using sentence-transformers (local, free)"

    def __init__(self,
                 model_name: str="all-MiniLM-L6-v2"):
        """
        Initialize the embedder
        Args:
            model_name: HuggingFace model name.
                         "all-MiniLM-L6-v2" is fast and good quality.
        """
        self.model= SentenceTransformer(model_name)

    def embed(self, text: List[str])-> np.ndarray:
        """
        Args:
            texts: List of strings to embed

        Returns:
            numpy array of shape (len(texts), embedding_dim)
        """
        return self.model.encode(text, convert_to_numpy=True)

    def embed_single(self, text: str) -> np.ndarray:
        """Generate embedding for single text"""
        return self.embed([text])[0]