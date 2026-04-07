from __future__ import annotations

from fastapi import APIRouter, Depends

from app.dependencies import chat_service, embedding_service, vector_store_service
from app.schemas import QueryRequest, QueryResponse, SourceChunk
from app.services.chat_service import ChatService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/query", response_model=QueryResponse)
def query(
    payload: QueryRequest,
    embedder: EmbeddingService = Depends(embedding_service),
    vector_store: VectorStoreService = Depends(vector_store_service),
    chat: ChatService = Depends(chat_service),
) -> QueryResponse:
    query_vector = embedder.embed_texts([payload.query])[0]
    hits = vector_store.search(query_vector=query_vector, top_k=payload.top_k)
    answer = chat.answer(query=payload.query, sources=hits)

    return QueryResponse(
        answer=answer,
        sources=[SourceChunk.model_validate(item) for item in hits],
    )
