from __future__ import annotations

from functools import lru_cache

from app.core.config import Settings, get_settings
from app.services.chat_service import ChatService
from app.services.embedding_service import EmbeddingService
from app.services.pdf_service import PdfService
from app.services.storage_service import StorageService
from app.services.vector_store_service import VectorStoreService


@lru_cache
def settings() -> Settings:
    return get_settings()


@lru_cache
def storage_service() -> StorageService:
    return StorageService(root=settings().storage_root)


@lru_cache
def pdf_service() -> PdfService:
    return PdfService()


@lru_cache
def embedding_service() -> EmbeddingService:
    cfg = settings()
    return EmbeddingService(model_name=cfg.embedding_model, dim=cfg.embedding_dim)


@lru_cache
def vector_store_service() -> VectorStoreService:
    cfg = settings()
    return VectorStoreService(
        qdrant_url=cfg.qdrant_url,
        collection_name=cfg.qdrant_collection,
        vector_size=cfg.embedding_dim,
    )


@lru_cache
def chat_service() -> ChatService:
    cfg = settings()
    return ChatService(base_url=cfg.ollama_base_url, model=cfg.ollama_model)
