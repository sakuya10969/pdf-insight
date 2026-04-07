# データベース設計

## 概要

従来のRDBは使用しない。ベクトルDBとしてQdrantのみ、docker-composeで起動する。

## Qdrant

### コレクション: `documents`

| フィールド | 型 | 説明 |
|-----------|-----|------|
| id | UUID | Qdrantポイント ID（自動生成） |
| vector | float[] | 384次元の埋め込み（all-MiniLM-L6-v2） |
| payload.doc_id | str | 親ドキュメントのUUID |
| payload.chunk_index | int | ドキュメント内のチャンク位置 |
| payload.text | str | チャンクテキスト |
| payload.metadata | dict | ページ番号、見出し等 |

### docker-compose設定

```yaml
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  qdrant_data:
```

### 備考
- コレクションはアプリ起動時に存在しなければ作成
- 距離メトリクス: Cosine
- ドキュメント削除時はdoc_idフィルタでベクトルを削除
- PoC段階ではレプリケーション・シャーディング不要
