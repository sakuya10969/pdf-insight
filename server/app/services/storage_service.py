from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fastapi import UploadFile

from app.schemas import DocumentRecord


class StorageService:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.pdf_dir = self.root / "pdfs"
        self.json_dir = self.root / "json"
        self.meta_file = self.root / "documents.json"

        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        self.json_dir.mkdir(parents=True, exist_ok=True)
        self.root.mkdir(parents=True, exist_ok=True)
        if not self.meta_file.exists():
            self.meta_file.write_text("[]", encoding="utf-8")

    async def save_pdf(self, file: UploadFile) -> tuple[str, Path]:
        doc_id = uuid.uuid4().hex
        ext = Path(file.filename or "document.pdf").suffix or ".pdf"
        target = self.pdf_dir / f"{doc_id}{ext}"
        content = await file.read()
        target.write_bytes(content)
        return doc_id, target

    def save_chunks_json(self, doc_id: str, chunks: list[dict]) -> Path:
        target = self.json_dir / f"{doc_id}.json"
        target.write_text(
            json.dumps({"doc_id": doc_id, "chunks": chunks}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return target

    def list_documents(self) -> list[DocumentRecord]:
        payload = json.loads(self.meta_file.read_text(encoding="utf-8"))
        records = [DocumentRecord.model_validate(item) for item in payload]
        return sorted(records, key=lambda x: x.uploaded_at, reverse=True)

    def upsert_document(
        self,
        doc_id: str,
        filename: str,
        status: str,
        chunk_count: int = 0,
        uploaded_at: datetime | None = None,
    ) -> DocumentRecord:
        records = self.list_documents()
        timestamp = uploaded_at or datetime.now(UTC)

        replaced = False
        updated: list[DocumentRecord] = []
        for record in records:
            if record.doc_id == doc_id:
                updated.append(
                    DocumentRecord(
                        doc_id=doc_id,
                        filename=filename,
                        status=status,
                        chunk_count=chunk_count,
                        uploaded_at=record.uploaded_at,
                    )
                )
                replaced = True
                continue
            updated.append(record)

        if not replaced:
            updated.append(
                DocumentRecord(
                    doc_id=doc_id,
                    filename=filename,
                    status=status,
                    chunk_count=chunk_count,
                    uploaded_at=timestamp,
                )
            )

        self.meta_file.write_text(
            json.dumps([record.model_dump(mode="json") for record in updated], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return next(record for record in updated if record.doc_id == doc_id)

    def delete_document_files(self, doc_id: str) -> None:
        for pdf_path in self.pdf_dir.glob(f"{doc_id}.*"):
            pdf_path.unlink(missing_ok=True)
        (self.json_dir / f"{doc_id}.json").unlink(missing_ok=True)

    def remove_document_from_meta(self, doc_id: str) -> bool:
        records = self.list_documents()
        remaining = [record for record in records if record.doc_id != doc_id]
        deleted = len(records) != len(remaining)
        self.meta_file.write_text(
            json.dumps([record.model_dump(mode="json") for record in remaining], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return deleted
