from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class DocumentRecord(BaseModel):
    doc_id: str
    filename: str
    status: str
    chunk_count: int = 0
    uploaded_at: datetime


class UploadResponse(BaseModel):
    document: DocumentRecord


class DocumentListResponse(BaseModel):
    documents: list[DocumentRecord]


class DeleteDocumentResponse(BaseModel):
    doc_id: str
    deleted: bool


class QueryRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class SourceChunk(BaseModel):
    doc_id: str
    chunk_id: str
    text: str
    page: int | None = None
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
