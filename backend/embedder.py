from typing import List, Dict, Any
import numpy as np
from fastembed import TextEmbedding
from backend.config import settings

class FastEmbedManager:
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL):
        self.model_name = model_name
        self.model = TextEmbedding(model_name=model_name)
        # Verifica a dimensão real gerando um embedding de teste
        sample = list(self.model.embed(["probe"]))[0]
        self.dimension = len(sample)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Gera vetores para múltiplos textos (chunks)"""
        if not texts:
            return []
        embeddings = list(self.model.embed(texts))
        return [emb.tolist() for emb in embeddings]

    def embed_query(self, query: str) -> List[float]:
        """Gera vetor para a pergunta do usuário"""
        emb = list(self.model.embed([query]))[0]
        return emb.tolist()

    def get_embedding_preview(self, vector: List[float]) -> Dict[str, Any]:
        """Gera representação didática e resumida do vetor de alta dimensão"""
        vec_arr = np.array(vector, dtype=float)
        norm = float(np.linalg.norm(vec_arr))
        return {
            "model": self.model_name,
            "dimension": len(vector),
            "norm_l2": round(norm, 4),
            "min_val": round(float(np.min(vec_arr)), 5),
            "max_val": round(float(np.max(vec_arr)), 5),
            "mean_val": round(float(np.mean(vec_arr)), 5),
            "first_5_values": [round(v, 5) for v in vector[:5]],
            "last_5_values": [round(v, 5) for v in vector[-5:]]
        }

embedder = FastEmbedManager()
