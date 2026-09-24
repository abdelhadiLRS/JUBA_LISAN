from __future__ import annotations

import re

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.core.limiter import limiter
from app.services.llm_adapter import LLMError, LLMUnavailableError, LLMTimeoutError, llm_adapter

router = APIRouter(prefix="/api/translate", tags=["translation"])

MAX_TRANSLATION_CHARS = 2000

LANGUAGE_NAMES = {
    "en": "English", "es": "Spanish", "it": "Italian", "pt": "Portuguese",
    "fr": "French", "de": "German", "ja": "Japanese", "ko": "Korean",
    "zh": "Chinese", "ar": "Arabic", "ru": "Russian", "nl": "Dutch",
    "pl": "Polish", "da": "Danish", "el": "Greek", "sv": "Swedish",
    "no": "Norwegian", "fi": "Finnish", "cs": "Czech",
}

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_TRANSLATION_CHARS)
    source: str = Field(default="auto", min_length=2, max_length=10)
    target: str = Field(default="ar", min_length=2, max_length=10)

class TranslationResponse(BaseModel):
    translation: str
    source: str
    target: str

def _normalize_language(code: str) -> str:
    return code.strip().lower().split("-")[0]

def _guess_source(text: str) -> str:
    if re.search(r"[\\u0600-\\u06ff]", text): return "ar"
    if re.search(r"[\\u3040-\\u30ff]", text): return "ja"
    if re.search(r"[\\uac00-\\ud7af]", text): return "ko"
    if re.search(r"[\\u4e00-\\u9fff]", text): return "zh"
    if re.search(r"[\\u0370-\\u03ff]", text): return "el"
    if re.search(r"[\\u0400-\\u04ff]", text): return "ru"
    return "en"

def _language_name(code: str) -> str:
    return LANGUAGE_NAMES.get(code, code)

def _clean_translation(value: str) -> str:
    value = value.strip()
    value = re.sub(r"^```(?:text|txt)?\\s*", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\\s*```$", "", value)
    return value.strip()

@router.post("", response_model=TranslationResponse)
@limiter.limit("30/minute")
async def translate(request: Request, payload: TranslationRequest) -> TranslationResponse:
    source = _normalize_language(payload.source)
    target = _normalize_language(payload.target)
    if source == "auto": source = _guess_source(payload.text)
    if target not in LANGUAGE_NAMES: raise HTTPException(status_code=400, detail="Unsupported target language")
    if source == target:
        return TranslationResponse(translation=payload.text.strip(), source=source, target=target)
    source_name = _language_name(source)
    target_name = _language_name(target)
    messages = [
        {"role": "system", "content": "You are JUBA LISAN's professional translation engine. Translate the user's text accurately and naturally. Preserve meaning, tone, punctuation, numbers, names, line breaks, and formatting. Do not explain the translation. Do not add notes. Return only the translated text."},
        {"role": "user", "content": "Translate from " + source_name + " (" + source + ") to " + target_name + " (" + target + ").\\nReturn only the translation.\\n\\n" + payload.text.strip()},
    ]
    try:
        result = await llm_adapter.chat(messages, stream=False)
        translation = _clean_translation(str(result))
        if not translation: raise LLMError("The translation service returned an empty response")
        return TranslationResponse(translation=translation, source=source, target=target)
    except (LLMTimeoutError, LLMUnavailableError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except LLMError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Translation service error: {exc}") from exc
