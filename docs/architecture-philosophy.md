# アーキテクチャ思想

## フロントエンド — Feature-Sliced Design（FSD）

技術的な役割ではなく、機能単位でコードを整理する。

```
app/
├── routes/       # ページコンポーネント（React Routerルート）
├── features/     # 機能モジュール（pdf-upload, search）
├── entities/     # ドメインデータモデル・UI（document）
└── shared/       # 共通UIコンポーネント・ユーティリティ
```

依存ルール: `routes → features → entities → shared`（上から下への一方向のみ）

各featureは自己完結型で、独自のUI・hooks・API呼び出しを持つ。sharedレイヤーは共通コンポーネントとユーティリティを提供する。

## バックエンド — モジュラーモノリス

単一デプロイ可能なユニットだが、内部はドメインモジュールで整理する。

```
server/
└── app/
    ├── main.py            # エントリポイント
    ├── modules/
    │   ├── storage/       # ローカルファイル管理
    │   ├── pdf/           # PDF解析・チャンク分割
    │   ├── embedding/     # 埋め込み生成
    │   ├── vector_store/  # Qdrant操作
    │   └── chat/          # LLM回答生成
    └── core/              # 設定、DI、ミドルウェア
```

各モジュールの構成:
- `router.py` — APIエンドポイント（外部公開する場合）
- `service.py` — ビジネスロジック
- `schemas.py` — Pydanticモデル

モジュール間はサービスのimportで連携する（HTTPではない）。境界を明確に保ち、必要に応じてマイクロサービスに分離可能にする。

## 基本方針

- シンプルさ優先 — PoC段階、過度な抽象化を避ける
- 型安全性 — TypeScript strict、Python型ヒント必須
- バックエンドは非同期（async/await）がデフォルト
- ローカルファーストのストレージ、クラウド置き換え可能なインターフェース
