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
    "no": "Norwegian", "fi": "Finnish", "cs": "Czech", "tr": "Turkish",
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
    """Detect the most likely source language locally and deterministically."""
    value = text.strip().lower()

    # Non-Latin scripts are high-confidence signals.
    if re.search(r"[\u0600-\u06ff]", value): return "ar"
    if re.search(r"[\u3040-\u30ff]", value): return "ja"
    if re.search(r"[\uac00-\ud7af]", value): return "ko"
    if re.search(r"[\u4e00-\u9fff]", value): return "zh"
    if re.search(r"[\u0370-\u03ff]", value): return "el"
    if re.search(r"[\u0400-\u04ff]", value): return "ru"

    # Latin-script languages need lexical/orthographic signals.
    patterns = {
        "fr": r"\b(bonjour|merci|avec|pour|dans|une|des|les|est|sont|être|français)\b|[àâçéèêëîïôùûüÿœ]",
        "es": r"\b(hola|gracias|para|como|qué|que|los|las|una|uno|está|español)\b|[áéíóúüñ¿¡]",
        "pt": r"\b(olá|obrigado|obrigada|para|como|você|vocês|uma|não|português)\b|[ãõáàâçêéíóôú]",
        "it": r"\b(ciao|grazie|perché|come|questa|questo|sono|una|uno|italiano)\b|[àèéìíîòóù]",
        "de": r"\b(hallo|danke|bitte|und|der|die|das|ein|eine|nicht|deutsch)\b|[äöüß]",
        "nl": r"\b(hallo|dank|voor|een|het|van|niet|nederlands)\b",
        "pl": r"\b(cześć|dzień|dziękuję|proszę|jest|nie|jeden|polski)\b|[ąćęłńóśźż]",
        "tr": r"\b(merhaba|teşekkür|lütfen|için|bir|bu|değil|türkçe)\b|[çğıöşü]",
        "da": r"\b(hej|tak|ikke|det|jeg|du|en|et|dansk)\b|[æøå]",
        "sv": r"\b(hej|tack|och|inte|det|jag|du|en|ett|svenska)\b|[åäö]",
        "no": r"\b(hei|takk|og|ikke|det|jeg|du|en|et|norsk)\b|[æøå]",
        "fi": r"\b(hei|kiitos|ja|ei|minä|sinä|suomi|suomen)\b|[äö]",
        "cs": r"\b(ahoj|děkuji|prosím|pro|jsem|není|čeština)\b|[ěščřžýáíéůúďťň]",
    }
    for language, pattern in patterns.items():
        if re.search(pattern, value, flags=re.IGNORECASE):
            return language
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
