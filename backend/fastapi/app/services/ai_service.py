from __future__ import annotations

from typing import Any, Dict

from openai import AsyncOpenAI, OpenAIError

from app.config import settings


class AIService:
    """Centralized AI client used by the API layer."""

    def __init__(self) -> None:
        self.api_key = settings.OPENAI_API_KEY
        self.client: AsyncOpenAI | None = None

        if self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)

    async def get_prediction(self, input_data: Dict[str, Any], model: str) -> Dict[str, Any]:
        """Send content to the configured AI model and return a normalized result."""

        if not self.client:
            # Provide a deterministic fallback when no provider key is configured.
            return {
                "result": f"Echo: {input_data.get('text', '').strip()}",
                "confidence": 0.5,
            }

        try:
            response = await self.client.responses.create(
                model=model,
                input=[{"role": "user", "content": input_data.get("text", "")}],
                max_output_tokens=200,
            )

            output_text = response.output[0].content[0].text if response.output else ""

            return {
                "result": output_text or "Empty response from model",
                "confidence": None,
            }
        except OpenAIError as exc:  # pragma: no cover - network dependent
            return {"error": f"Model call failed: {exc}"}
