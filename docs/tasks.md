# タスク一覧

## フェーズ1: インフラ構築
- [ ] docker-compose.yml作成（Qdrant）
- [ ] FastAPIエントリポイント + uvicorn設定
- [ ] CORS設定・ヘルスチェックエンドポイント
- [ ] core/config.py（環境変数管理）
- [ ] Mantine + AppShellルートレイアウト構築

## フェーズ2: ストレージ・PDFモジュール
- [ ] StorageService実装（PDF/JSONの保存・読込・削除）
- [ ] PdfService実装（PyMuPDF4LLM解析、チャンク分割）
- [ ] PDFアップロードエンドポイント（POST /api/pdf/upload）
- [ ] ドキュメント一覧エンドポイント（GET /api/pdf/documents）
- [ ] ドキュメント削除エンドポイント（DELETE /api/pdf/documents/{doc_id}）

## フェーズ3: 埋め込み・ベクトルストア
- [ ] EmbeddingService実装（Sentence-Transformers）
- [ ] VectorStoreService実装（Qdrant CRUD）
- [ ] Qdrantコレクション起動時作成
- [ ] 取り込みパイプライン接続（解析 → 埋め込み → 登録）

## フェーズ4: 検索・チャット
- [ ] ChatService実装（Ollama連携）
- [ ] 検索エンドポイント（POST /api/chat/query）
- [ ] 検索ページUI（クエリ入力、結果表示、LLM回答）

## フェーズ5: フロントエンド機能
- [ ] PDFアップロードページ（ドロップゾーン、進捗、ドキュメント一覧）
- [ ] ドキュメント管理UI（一覧、削除、ステータス）
- [ ] フロントエンド ↔ バックエンドAPI接続（Axios + TanStack Query）
