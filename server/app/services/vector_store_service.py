from __future__ import annotations

from qdrant_client import QdrantClient, models


class VectorStoreService:
    def __init__(self, qdrant_url: str, collection_name: str, vector_size: int) -> None:
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.client = QdrantClient(url=qdrant_url)

    def ensure_collection(self) -> None:
        collections = self.client.get_collections().collections
        exists = any(collection.name == self.collection_name for collection in collections)
        if exists:
            return
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=self.vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    def upsert_chunks(self, doc_id: str, chunks: list[dict], vectors: list[list[float]]) -> None:
        points = []
        for idx, (chunk, vector) in enumerate(zip(chunks, vectors, strict=False)):
            points.append(
                models.PointStruct(
                    id=f"{doc_id}-{idx}",
                    vector=vector,
                    payload={
                        "doc_id": doc_id,
                        "chunk_id": chunk["chunk_id"],
                        "text": chunk["text"],
                        "page": chunk.get("page"),
                    },
                )
            )

        if points:
            self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_vector: list[float], top_k: int) -> list[dict]:
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
        )
        payloads: list[dict] = []
        for item in results:
            payload = item.payload or {}
            payloads.append(
                {
                    "doc_id": payload.get("doc_id", ""),
                    "chunk_id": payload.get("chunk_id", ""),
                    "text": payload.get("text", ""),
                    "page": payload.get("page"),
                    "score": float(item.score),
                }
            )
        return payloads

    def delete_document(self, doc_id: str) -> None:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.Filter(
                must=[
                    models.FieldCondition(
                        key="doc_id",
                        match=models.MatchValue(value=doc_id),
                    )
                ]
            ),
        )
