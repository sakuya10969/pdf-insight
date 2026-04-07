# ドメイン設計

## エンティティ

### Document（ドキュメント）
アップロードされたPDFとその処理状態を表す。

| フィールド | 型 | 説明 |
|-----------|-----|------|
| doc_id | UUID | 一意な識別子 |
| filename | str | 元のファイル名 |
| status | enum | `processing`, `ready`, `error` |
| chunk_count | int | 解析後のチャンク数 |
| created_at | datetime | アップロード日時 |

DBテーブルなし — ファイルシステム（`data/pdfs/`, `data/json/`）から導出する。

### Chunk（チャンク）
PDF解析後のコンテンツ断片。

| フィールド | 型 | 説明 |
|-----------|-----|------|
| doc_id | UUID | 親ドキュメントID |
| chunk_index | int | ドキュメント内の位置 |
| text | str | チャンクテキスト |
| metadata | dict | ページ番号、セクション見出し等 |

JSONファイル（`data/json/{doc_id}.json`）およびQdrantポイントとして保存。

### SearchResult（検索結果）
ベクトル検索から返される結果。

| フィールド | 型 | 説明 |
|-----------|-----|------|
| doc_id | UUID | ソースドキュメント |
| chunk_index | int | チャンク位置 |
| text | str | マッチしたチャンクテキスト |
| score | float | 類似度スコア |

## サービス

| サービス | モジュール | 責務 |
|---------|-----------|------|
| StorageService | app.modules.storage | doc_id単位でPDF/JSONファイルの保存・読込・削除 |
| PdfService | app.modules.pdf | PDF解析、チャンク生成、取り込みパイプラインの統括 |
| EmbeddingService | app.modules.embedding | Sentence-Transformersによる埋め込み生成 |
| VectorStoreService | app.modules.vector_store | Qdrantコレクションに対するCRUD操作 |
| ChatService | app.modules.chat | コンテキストチャンクでプロンプト構築、Ollama呼び出し、回答返却 |

## データフロー

```
アップロード: PDF → PdfService.parse() → chunks[]
              → EmbeddingService.embed()
              → VectorStoreService.upsert() + StorageService.save()

検索: query → EmbeddingService.embed()
      → VectorStoreService.search() → chunks[]
      → ChatService.generate_answer()
```
