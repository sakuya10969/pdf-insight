from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.dependencies import (
    embedding_service,
    pdf_service,
    storage_service,
    vector_store_service,
)
from app.schemas import DeleteDocumentResponse, DocumentListResponse, UploadResponse
from app.services.embedding_service import EmbeddingService
from app.services.pdf_service import PdfService
from app.services.storage_service import StorageService
from app.services.vector_store_service import VectorStoreService

router = APIRouter(prefix="/api/pdf", tags=["pdf"])


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    storage: StorageService = Depends(storage_service),
    pdf_parser: PdfService = Depends(pdf_service),
    embedder: EmbeddingService = Depends(embedding_service),
    vector_store: VectorStoreService = Depends(vector_store_service),
) -> UploadResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDFファイルのみアップロード可能です")

    doc_id, pdf_path = await storage.save_pdf(file)
    storage.upsert_document(
        doc_id=doc_id,
        filename=file.filename,
        status="processing",
        chunk_count=0,
    )

    try:
        chunks = pdf_parser.parse_pdf(pdf_path)
        if not chunks:
            raise HTTPException(status_code=400, detail="PDFからテキストを抽出できませんでした")

        storage.save_chunks_json(doc_id=doc_id, chunks=chunks)
        vectors = embedder.embed_texts([chunk["text"] for chunk in chunks])
        vector_store.upsert_chunks(doc_id=doc_id, chunks=chunks, vectors=vectors)

        record = storage.upsert_document(
            doc_id=doc_id,
            filename=file.filename,
            status="ready",
            chunk_count=len(chunks),
        )
    except HTTPException:
        storage.upsert_document(
            doc_id=doc_id,
            filename=file.filename,
            status="failed",
            chunk_count=0,
        )
        raise
    except Exception as exc:
        storage.upsert_document(
            doc_id=doc_id,
            filename=file.filename,
            status="failed",
            chunk_count=0,
        )
        raise HTTPException(status_code=500, detail=f"アップロード処理に失敗しました: {exc}") from exc

    return UploadResponse(document=record)


@router.get("/documents", response_model=DocumentListResponse)
def list_documents(
    storage: StorageService = Depends(storage_service),
) -> DocumentListResponse:
    return DocumentListResponse(documents=storage.list_documents())


@router.delete("/documents/{doc_id}", response_model=DeleteDocumentResponse)
def delete_document(
    doc_id: str,
    storage: StorageService = Depends(storage_service),
    vector_store: VectorStoreService = Depends(vector_store_service),
) -> DeleteDocumentResponse:
    vector_store.delete_document(doc_id)
    storage.delete_document_files(doc_id)
    deleted = storage.remove_document_from_meta(doc_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="対象ドキュメントが見つかりません")
    return DeleteDocumentResponse(doc_id=doc_id, deleted=True)
