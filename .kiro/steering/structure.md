# プロジェクト構成

## ディレクトリ構造

```
├── client/                     # フロントエンド（React Router）
│   ├── app/
│   │   ├── app.css
│   │   ├── root.tsx            # ルートレイアウト
│   │   ├── routes.ts           # ルート定義
│   │   ├── routes/             # ページコンポーネント
│   │   │   └── home.tsx
│   │   ├── features/           # FSD: 機能単位モジュール（今後追加）
│   │   │   ├── pdf-upload/     # PDFアップロード機能
│   │   │   └── search/         # 検索・チャット機能
│   │   ├── shared/             # FSD: 共通UI・ユーティリティ
│   │   │   ├── ui/
│   │   │   └── lib/
│   │   └── entities/           # FSD: ドメインエンティティ
│   │       └── document/
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── data/                       # ローカルファイルストレージ
│   ├── pdfs/                   # アップロードされたPDFファイル
│   │   └── {doc_id}.pdf
│   └── json/                   # PDF解析結果（チャンク情報JSON）
│       └── {doc_id}.json
│
├── server/                     # バックエンド（FastAPI）
│   ├── app/
│   │   ├── main.py             # エントリポイント
│   │   ├── modules/            # モジュラーモノリス: 機能モジュール
│   │   │   ├── storage/        # ローカルファイルストレージ管理
│   │   │   │   ├── service.py
│   │   │   │   └── schemas.py
│   │   │   ├── pdf/            # PDF解析・チャンク分割
│   │   │   │   ├── router.py
│   │   │   │   ├── service.py
│   │   │   │   └── schemas.py
│   │   │   ├── embedding/      # 埋め込み生成
│   │   │   │   ├── service.py
│   │   │   │   └── schemas.py
│   │   │   ├── vector_store/   # Qdrant操作
│   │   │   │   ├── service.py
│   │   │   │   └── schemas.py
│   │   │   └── chat/           # LLM回答生成
│   │   │       ├── router.py
│   │   │       ├── service.py
│   │   │       └── schemas.py
│   │   └── core/               # 共通設定・ユーティリティ
│   │       ├── config.py
│   │       └── dependencies.py
│   ├── pyproject.toml
│   └── .python-version
│
└── .kiro/
    └── steering/
        ├── product.md          # プロダクト概要
        ├── tech.md             # 技術構成
        └── structure.md        # プロジェクト構成（このファイル）
```

## FSD（Feature-Sliced Design）レイヤー

フロントエンドはFSDアーキテクチャに従う:

| レイヤー | 役割 | 例 |
|---------|------|-----|
| `routes/` | ページコンポーネント（React Routerのルート） | `home.tsx` |
| `features/` | ユーザ操作に対応する機能単位 | `pdf-upload/`, `search/` |
| `entities/` | ビジネスドメインのデータモデル・UI | `document/` |
| `shared/` | 再利用可能なUI・ユーティリティ | `ui/`, `lib/` |

依存方向: `routes → features → entities → shared`（上位から下位への一方向のみ）

## モジュラーモノリス（バックエンド）

バックエンドは機能単位でモジュール分割:

| モジュール | 責務 |
|-----------|------|
| `storage` | ローカルファイルシステムでのPDF/JSON管理（doc_id単位） |
| `pdf` | PDFアップロード受付、解析、チャンク分割 |
| `embedding` | Sentence-Transformersによる埋め込み生成 |
| `vector_store` | Qdrantへの登録・検索 |
| `chat` | クエリ受付、コンテキスト構築、Ollamaによる回答生成 |
| `core` | 共通設定、DI、ミドルウェア |

各モジュールは `router.py`（APIエンドポイント）、`service.py`（ビジネスロジック）、`schemas.py`（Pydanticモデル）で構成する。

## ストレージ設計

### ディレクトリ構成

```
data/
├── pdfs/           # アップロードされたPDFファイル
│   └── {doc_id}.pdf
└── json/           # PDF解析結果（チャンク情報）
    └── {doc_id}.json
```

### 設計方針
- doc_idはUUIDを使用し、PDFとJSONを同一IDで紐付ける
- JSONはPDF解析結果のキャッシュ用途（再embeddingやデバッグに再利用）
- ファイル操作はdoc_id単位（削除・更新時にPDF/JSON/Qdrantを一括処理）
- Qdrantとの整合性はdoc_idで担保
- RDB・クラウドストレージは使用しない（PoC段階）
- 後からクラウドストレージに置き換え可能な抽象化を意識する
