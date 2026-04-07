# 技術構成

## フロントエンド

- フレームワーク: React Router v7（SSR有効）
- アーキテクチャ: FSD（Feature-Sliced Design）
- スタイリング: Tailwind CSS v4
- ビルドツール: Vite v8
- 言語: TypeScript（strict mode）
- パッケージマネージャ: bun

## バックエンド

- フレームワーク: FastAPI
- アーキテクチャ: モジュラーモノリス
- 言語: Python 3.12+
- パッケージマネージャ: uv

## インフラ・外部サービス

- ベクトルDB: Qdrant
- 埋め込みモデル: Sentence-Transformers（all-MiniLM-L6-v2）
- チャットモデル: Ollama（llama3 / qwen）
- PDF解析: PyMuPDF4LLM
- コンテナ: Docker

## 開発規約

### Python（バックエンド）
- 型ヒント必須
- Pydanticモデルでリクエスト/レスポンスを定義
- 非同期（async/await）を基本とする
- テスト: pytest

### TypeScript（フロントエンド）
- strict modeを維持
- パスエイリアス `~/` を使用（`app/` にマッピング）
- コンポーネントは関数コンポーネントのみ
- テスト: vitest
