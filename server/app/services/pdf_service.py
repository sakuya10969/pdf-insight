from __future__ import annotations

from pathlib import Path

import fitz


class PdfService:
    def __init__(self, max_chunk_chars: int = 1200) -> None:
        self.max_chunk_chars = max_chunk_chars

    def parse_pdf(self, pdf_path: Path) -> list[dict]:
        markdown_text = self._extract_markdown(pdf_path)

        if markdown_text.strip():
            chunks = self._split_text(markdown_text)
            return [
                {"chunk_id": f"chunk-{idx}", "text": text, "page": None}
                for idx, text in enumerate(chunks)
            ]

        page_chunks: list[dict] = []
        with fitz.open(pdf_path) as doc:
            for page_idx, page in enumerate(doc, start=1):
                content = page.get_text("text").strip()
                if not content:
                    continue
                for idx, piece in enumerate(self._split_text(content)):
                    page_chunks.append(
                        {
                            "chunk_id": f"p{page_idx}-chunk-{idx}",
                            "text": piece,
                            "page": page_idx,
                        }
                    )
        return page_chunks

    def _extract_markdown(self, pdf_path: Path) -> str:
        try:
            import pymupdf4llm

            return str(pymupdf4llm.to_markdown(str(pdf_path)))
        except Exception:
            return ""

    def _split_text(self, text: str) -> list[str]:
        normalized = "\n".join(line.strip() for line in text.splitlines() if line.strip())
        if not normalized:
            return []

        blocks: list[str] = []
        current: list[str] = []
        current_len = 0

        for paragraph in normalized.split("\n"):
            p_len = len(paragraph)
            if current and current_len + p_len > self.max_chunk_chars:
                blocks.append("\n".join(current))
                current = [paragraph]
                current_len = p_len
            else:
                current.append(paragraph)
                current_len += p_len

        if current:
            blocks.append("\n".join(current))

        return blocks
