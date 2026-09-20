from __future__ import annotations

import os
from typing import Any


class AIProvider:
    def generate_suggestions(self, history: list[dict], current_user_id: str) -> list[str]:
        if not history:
            return [
                "Hey! Would you like to grab coffee sometime?",
                "I’d love to get to know you better over a casual chat.",
                "What kind of things do you enjoy doing on weekends?",
            ]

        recent_text = " ".join(
            str(item.get("content", ""))
            for item in history[-6:]
        )
        lower_text = recent_text.lower()

        suggestions = [
            "That sounds great — want to continue the conversation over coffee?",
            "I’d enjoy that too. What’s your favorite place to spend a relaxed afternoon?",
            "I like that idea. Want to plan something around your interests?",
        ]

        if "coffee" in lower_text or "cafe" in lower_text or "coffee" in lower_text:
            suggestions[0] = "Coffee sounds perfect. Want to meet for a quick café catch-up?"
            suggestions[1] = "I’d be down for coffee and a casual chat — what time works for you?"

        if "museum" in lower_text or "art" in lower_text or "gallery" in lower_text:
            suggestions[0] = "A museum or gallery date sounds fun — would you be up for that?"
            suggestions[2] = "I’d love to explore a museum with you sometime."

        if "weekend" in lower_text:
            suggestions[1] = "This weekend could work well — do you have a favorite spot in mind?"

        return suggestions[:3]


class AIService:
    def __init__(self, provider: AIProvider | None = None):
        self.provider = provider or AIProvider()

    def generate_message_suggestions(self, history: list[dict], current_user_id: str):
        provider_name = os.getenv("AI_PROVIDER", "local").lower()

        if provider_name == "openai":
            return self._generate_via_openai(history, current_user_id)

        return self.provider.generate_suggestions(history, current_user_id)

    def _generate_via_openai(self, history: list[dict], current_user_id: str):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return self.provider.generate_suggestions(history, current_user_id)

        try:
            import openai

            prompt = self._build_prompt(history, current_user_id)
            response = openai.OpenAI(api_key=api_key).chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You are a dating app assistant that suggests short, warm, natural replies."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=120,
            )

            text = response.choices[0].message.content or ""
            suggestions = [line.strip(" -\n") for line in text.split("\n") if line.strip()]
            if len(suggestions) >= 3:
                return suggestions[:3]
        except Exception:
            pass

        return self.provider.generate_suggestions(history, current_user_id)

    def _build_prompt(self, history: list[dict], current_user_id: str) -> str:
        context = "\n".join(
            f"{message.get('sender_id')}: {message.get('content')}"
            for message in history[-8:]
        )
        return (
            "Suggest 3 concise, warm, natural reply options for a dating app conversation. "
            f"Current user id: {current_user_id}\nConversation:\n{context}"
        )


ai_service = AIService()
