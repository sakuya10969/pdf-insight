# API設計

ベースURL: `http://localhost:8000/api`

## PDFモジュール

### PDFアップロード
```
POST /api/pdf/upload
Content-Type: multipart/form-data
Body: file (PDF)

レスポンス 201:
{
  "doc_id": "uuid",
  "filename": "original.pdf",
  "status": "processing"
}
```

### ドキュメント一覧
```
GET /api/pdf/documents

レスポンス 200:
[
  {
    "doc_id": "uuid",
    "filename": "original.pdf",
    "status": "ready" | "processing" | "error",
    "chunk_count": 42,
    "created_at": "2026-04-07T00:00:00Z"
  }
]
```

### ドキュメント削除
```
DELETE /api/pdf/documents/{doc_id}

レスポンス 204
```
指定doc_idのPDFファイル、JSONキャッシュ、Qdrantベクトルを一括削除する。

## チャットモジュール

### 検索・回答生成
```
POST /api/chat/query
Content-Type: application/json
Body:
{
  "query": "主な結論は何ですか？",
  "top_k": 3
}

レスポンス 200:
{
  "answer": "主な結論は...",
  "sources": [
    {
      "doc_id": "uuid",
      "chunk_index": 5,
      "text": "該当チャンクのテキスト...",
      "score": 0.87
    }
  ]
}
```

## ヘルスチェック

```
GET /api/health

レスポンス 200:
{ "status": "ok" }
```
