# タスク一覧

## フェーズ1: インフラ構築
- [x] docker-compose.yml作成（Qdrant）
- [x] FastAPIエントリポイント + uvicorn設定
- [x] CORS設定・ヘルスチェックエンドポイント
- [x] core/config.py（環境変数管理）
- [x] Mantine + AppShellルートレイアウト構築

## フェーズ2: ストレージ・PDFモジュール
- [x] StorageService実装（PDF/JSONの保存・読込・削除）
- [x] PdfService実装（PyMuPDF4LLM解析、チャンク分割）
- [x] PDFアップロードエンドポイント（POST /api/pdf/upload）
- [x] ドキュメント一覧エンドポイント（GET /api/pdf/documents）
- [x] ドキュメント削除エンドポイント（DELETE /api/pdf/documents/{doc_id}）

## フェーズ3: 埋め込み・ベクトルストア
- [x] EmbeddingService実装（Sentence-Transformers）
- [x] VectorStoreService実装（Qdrant CRUD）
- [x] Qdrantコレクション起動時作成
- [x] 取り込みパイプライン接続（解析 → 埋め込み → 登録）

## フェーズ4: 検索・チャット
- [x] ChatService実装（Ollama連携）
- [x] 検索エンドポイント（POST /api/chat/query）
- [x] 検索ページUI（クエリ入力、結果表示、LLM回答）

## フェーズ5: フロントエンド機能
- [x] PDFアップロードページ（ドロップゾーン、進捗、ドキュメント一覧）
- [x] ドキュメント管理UI（一覧、削除、ステータス）
- [x] フロントエンド ↔ バックエンドAPI接続（Axios + TanStack Query）
