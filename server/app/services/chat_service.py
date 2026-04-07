from __future__ import annotations

from ollama import Client


class ChatService:
    def __init__(self, base_url: str, model: str) -> None:
        self.client = Client(host=base_url)
        self.model = model

    def answer(self, query: str, sources: list[dict]) -> str:
        if not sources:
            return "関連する情報が見つかりませんでした。"

        context = "\n\n".join(
            f"[source {idx + 1}] {source['text']}" for idx, source in enumerate(sources)
        )

        prompt = (
            "次のコンテキストのみを使って、質問に日本語で簡潔に答えてください。"
            "情報が不足する場合は不足していると明示してください。\n\n"
            f"質問: {query}\n\n"
            f"コンテキスト:\n{context}"
        )

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは与えられた資料だけで回答するアシスタントです。",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            return response["message"]["content"]
        except Exception:
            return "回答生成に失敗しました。Ollamaの接続状態を確認してください。"
