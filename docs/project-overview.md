# プロジェクト概要

## 概要

PDFドキュメントのRAG（Retrieval-Augmented Generation）システム。
PDFをアップロードし、内容をベクトル化して意味検索を行い、LLMで回答を生成する。

## フェーズ

PoC（Proof of Concept）段階。コアフローの実装と検証を優先する。

## コアフロー

### PDF取り込み
1. ユーザがPDFをアップロード
2. PyMuPDF4LLMでPDF解析 → 構造化JSON
3. 構造ベース + semantic補助でチャンク分割
4. Sentence-Transformersで埋め込み生成
5. Qdrantにチャンク登録（doc_idで紐付け）
6. PDFとJSONをローカルファイルシステムに保存

### 検索・回答
1. ユーザがクエリを入力
2. クエリをSentence-Transformersで埋め込み
3. Qdrantでベクトル検索（top-k=3）
4. 該当チャンクを取得
5. Ollamaで回答生成

## ストレージ方針

- ローカルファイルシステムのみ（RDB・クラウドストレージ不使用）
- `data/pdfs/{doc_id}.pdf` と `data/json/{doc_id}.json`
- doc_id（UUID）でPDF、JSON、Qdrantベクトルを紐付け
- 後からクラウドストレージに置き換え可能な設計
