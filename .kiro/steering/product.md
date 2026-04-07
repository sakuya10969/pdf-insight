# プロダクト概要

## PDF取り込み & 検索システム

PDFドキュメントをアップロードし、内容をベクトル化して意味検索を行い、LLMによる回答生成を提供するRAG（Retrieval-Augmented Generation）システム。

## 主要機能

### PDFアップロード・解析
- PDFファイルのアップロード
- PyMuPDF4LLMによるPDF解析・構造化（JSON化）
- 構造ベース + semantic補助によるチャンク分割
- Sentence-Transformersによる埋め込み生成
- Qdrantへのベクトル登録

### 検索・回答生成
- ユーザクエリの入力
- クエリの埋め込み生成
- ベクトル検索（top-k=3）
- 該当チャンクの取得
- Ollama（llama3 / qwen）によるLLM回答生成

## 開発フェーズ

現在はPoC（Proof of Concept）段階。基本的な処理フローの実装と検証を優先する。
