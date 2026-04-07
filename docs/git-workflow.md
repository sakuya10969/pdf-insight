# Git Workflow

## 1. 基本方針

- 単一ブランチ運用（main or develop）
- ブランチは切らない
- 直接pushのみ

---

## 2. Commit Rules

### Prefix（必須）

- feat: 新機能
- fix: バグ修正
- refactor: リファクタ
- docs: ドキュメント
- chore: 設定変更

### 例

feat: PDFアップロード追加  
fix: nullエラー修正  

---

## 3. ルール

- 1コミット = 1変更
- 動く状態でコミットする
- 無関係な変更を混ぜない

---

## 4. 禁止

- 意味不明なコミット
- 巨大コミット
- 動かない状態でのpush
- console.logの放置

---

## 5. 最低限の意識

- 小さく刻む
- 意図を明確にする
