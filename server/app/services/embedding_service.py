from __future__ import annotations

import hashlib
import math

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name: str, dim: int) -> None:
        self.model_name = model_name
        self.dim = dim
        self._model: SentenceTransformer | None = None

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        model = self._get_model()
        if model is None:
            return [self._fallback_embed(text) for text in texts]
        vectors = model.encode(texts, normalize_embeddings=True)
        return vectors.tolist()

    def _get_model(self) -> SentenceTransformer | None:
        if self._model is not None:
            return self._model
        try:
            self._model = SentenceTransformer(self.model_name)
            return self._model
        except Exception:
            return None

    def _fallback_embed(self, text: str) -> list[float]:
        values: list[float] = []
        seed = text.encode("utf-8")
        while len(values) < self.dim:
            seed = hashlib.sha256(seed).digest()
            values.extend((byte / 127.5) - 1 for byte in seed)
        trimmed = values[: self.dim]
        norm = math.sqrt(sum(v * v for v in trimmed)) or 1.0
        return [v / norm for v in trimmed]
