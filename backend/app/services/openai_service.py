"""OpenAI Service for AI Tutor functionality"""
from __future__ import annotations

import json
from typing import Any

from app.core.app_logger import get_logger
from app.core.config import settings
from app.services.llm_adapter import LLMAdapter

logger = get_logger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API for language tutoring"""

    def __init__(self):
        self.llm = LLMAdapter()
        self.default_model = "gpt-4o-mini"  # or your preferred model

    async def get_tutor_response(
        self,
        message: str,
        language: str,
        topic: str | None = None,
        conversation_history: list[dict[str, str]] | None = None,
        user_level: str = "intermediate",
    ) -> dict[str, Any]:
        """
        Get a response from the AI language tutor.

        Args:
            message: User's message
            language: Target language code (e.g., 'en', 'de', 'fr')
            topic: Conversation topic (optional)
            conversation_history: List of previous messages for context
            user_level: User's proficiency level (beginner, intermediate, advanced)

        Returns:
            Dictionary with 'response' and optionally 'suggested_topic'
        """
        # Build system prompt based on language and level
        system_prompt = self._build_system_prompt(language, user_level, topic)

        # Build conversation messages
        messages = []
        if conversation_history:
            messages.extend(conversation_history[-10:])  # Last 10 messages for context

        messages.append({"role": "user", "content": message})

        try:
            # Call LLM with structured output
            response_schema = {
                "type": "object",
                "properties": {
                    "response": {
                        "type": "string",
                        "description": "The tutor's response in the target language"
                    },
                    "suggested_topic": {
                        "type": "string",
                        "description": "Optional suggested follow-up topic"
                    },
                    "correction": {
                        "type": "string",
                        "description": "Optional correction of user's grammar/vocabulary"
                    },
                    "explanation": {
                        "type": "string",
                        "description": "Explanation in user's native language if needed"
                    }
                },
                "required": ["response"]
            }

            result = await self.llm.generate_structured(
                messages=messages,
                system_prompt=system_prompt,
                schema=response_schema,
                model=self.default_model
            )

            response_data = json.loads(result) if isinstance(result, str) else result

            return {
                "response": response_data.get("response", ""),
                "suggested_topic": response_data.get("suggested_topic"),
                "correction": response_data.get("correction"),
                "explanation": response_data.get("explanation")
            }

        except Exception as e:
            logger.error(f"Error getting tutor response: {e}")
            # Fallback response
            return {
                "response": f"I apologize, but I'm having trouble processing your message. Let's continue our conversation about {topic or 'language learning'}.",
                "suggested_topic": None
            }

    def _build_system_prompt(
        self,
        language: str,
        user_level: str,
        topic: str | None = None
    ) -> str:
        """Build system prompt for the AI tutor"""

        language_names = {
            "en": "English",
            "de": "German",
            "fr": "French",
            "es": "Spanish",
            "it": "Italian",
            "pt": "Portuguese",
            "nl": "Dutch",
            "pl": "Polish",
            "ru": "Russian",
            "ro": "Romanian",
            "ar": "Arabic"
        }

        lang_name = language_names.get(language, language)

        level_instructions = {
            "beginner": "Use simple vocabulary and short sentences. Explain concepts clearly and patiently.",
            "intermediate": "Use moderate vocabulary. Provide occasional corrections and explanations.",
            "advanced": "Use natural, native-level speech. Focus on nuanced corrections and cultural insights."
        }

        topic_context = f" The current topic is '{topic}'." if topic else ""

        return f"""You are JUBA LISAN, a friendly and encouraging AI language tutor specializing in teaching {lang_name}.

Your role:
- Engage in natural conversation to help the user practice {lang_name}
- Provide gentle corrections when the user makes mistakes
- Explain grammar, vocabulary, and cultural context when helpful
- Keep the conversation flowing naturally{topic_context}
- Adapt your language complexity to the user's level: {user_level}

Guidelines:
- {level_instructions.get(user_level, level_instructions['intermediate'])}
- Be patient, encouraging, and supportive
- Celebrate progress and small wins
- If the user struggles, offer simpler alternatives
- Occasionally suggest new topics to explore
- Use the target language ({lang_name}) primarily, but explain complex concepts in the user's native language if needed

Remember: Your goal is to make language learning enjoyable and effective!"""

    async def generate_conversation_topics(
        self,
        language: str,
        user_interests: list[str] | None = None,
        count: int = 5
    ) -> list[dict[str, str]]:
        """Generate personalized conversation topics"""

        system_prompt = f"""Generate {count} engaging conversation topics for learning {language}.
        Consider modern, relevant subjects that would interest language learners."""

        if user_interests:
            interests_str = ", ".join(user_interests)
            system_prompt += f" User interests include: {interests_str}."

        messages = [
            {"role": "user", "content": f"Generate {count} conversation topics for practicing {language}."}
        ]

        try:
            result = await self.llm.generate(
                messages=messages,
                system_prompt=system_prompt,
                model=self.default_model
            )

            # Parse the response (expecting JSON or formatted list)
            # In production, use structured output
            topics = []
            lines = result.strip().split('\n')
            for line in lines[:count]:
                if line.strip():
                    topics.append({"title": line.strip(), "language": language})

            return topics

        except Exception as e:
            logger.error(f"Error generating topics: {e}")
            # Return default topics
            return [
                {"title": "Daily routines and habits", "language": language},
                {"title": "Travel experiences", "language": language},
                {"title": "Food and cuisine", "language": language},
                {"title": "Hobbies and interests", "language": language},
                {"title": "Future plans and goals", "language": language}
            ]
