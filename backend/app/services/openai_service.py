"""Legacy tutor facade over the configured LLM adapter, not a fixed provider."""
from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field
from app.services.llm_adapter import LLMAdapter, LLMError


class TutorReply(BaseModel):
    response: str = Field(min_length=1)
    suggested_topic: str | None = None
    correction: str | None = None
    explanation: str | None = None


class OpenAIService:
    def __init__(self):
        self.llm = LLMAdapter()
        self.default_model = None

    async def get_tutor_response(self, message: str, language: str, topic: str | None = None,
                                conversation_history: list[dict[str, str]] | None = None,
                                user_level: str = "intermediate") -> dict[str, Any]:
        messages = [{"role": "system", "content": self._build_system_prompt(language, user_level, topic)}]
        messages.extend((conversation_history or [])[-10:])
        messages.append({"role": "user", "content": message})
        reply = await self.llm.structured_output(messages, TutorReply)
        if not reply.response.strip():
            raise LLMError("Tutor returned an empty response")
        return reply.model_dump()

    def _build_system_prompt(self, language: str, user_level: str, topic: str | None = None) -> str:
        names = {"en": "English", "de": "German", "fr": "French", "es": "Spanish", "it": "Italian", "pt": "Portuguese",
                 "nl": "Dutch", "pl": "Polish", "ru": "Russian", "ro": "Romanian", "ar": "Arabic"}
        instructions = {"beginner": "Use simple vocabulary and short sentences. Explain clearly and patiently.",
                        "intermediate": "Use moderate vocabulary. Provide occasional corrections and explanations.",
                        "advanced": "Use natural, native-level speech, nuanced corrections and cultural insights."}
        name = names.get(language, language)
        context = f" The current topic is {topic}." if topic else ""
        return (f"You are JUBA LISAN, a friendly language tutor for {name}. Engage in natural conversation. "
                f"Provide gentle grammar and vocabulary corrections, with brief explanations when helpful.{context} "
                f"Adapt to the student's level: {user_level}. {instructions.get(user_level, instructions['intermediate'])} "
                f"Be encouraging, celebrate progress and suggest follow-up topics. Primarily use {name}.")

    async def generate_conversation_topics(self, language: str, user_interests: list[str] | None = None, count: int = 5) -> list[dict[str, str]]:
        result = await self.llm.chat([{"role": "user", "content": f"Generate {count} short conversation topic titles for learning {language}. Interests: {', '.join(user_interests or [])}. Return one title per line."}], stream=False)
        return [{"title": line.strip(), "language": language} for line in str(result).splitlines() if line.strip()][:count]
