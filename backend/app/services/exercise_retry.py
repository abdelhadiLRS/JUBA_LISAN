from __future__ import annotations

from collections.abc import Sequence
import re
from typing import Literal

# Lower number = easier interaction. Unknown interaction types are left unchanged.
LOW_SCORE_THRESHOLD = 0.50
SUCCESS_SCORE_THRESHOLD = 0.80

ScoreClassification = Literal["low", "middle", "success"]


def classify_score(score: float) -> ScoreClassification:
    """Classify an exercise score using the shared adaptive thresholds."""
    if score < LOW_SCORE_THRESHOLD:
        return "low"
    if score >= SUCCESS_SCORE_THRESHOLD:
        return "success"
    return "middle"


DIFFICULTY: dict[str, int] = {
    "multiple_choice": 1,
    "fill_blank": 2,
    "translate": 3,
    "listening": 3,
    "pronunciation": 3,
    "free_write": 4,
}

ALIASES = {
    "choice": "multiple_choice",
    "mcq": "multiple_choice",
    "multiple-choice": "multiple_choice",
    "gap": "fill_blank",
    "fill-blank": "fill_blank",
    "writing": "free_write",
    "free-write": "free_write",
}


def normalise_variant(value: object) -> str:
    """Return a canonical variant name, safely ignoring malformed values."""
    if not isinstance(value, str):
        return ""
    raw = re.sub(r"[\s_]+", "-", value.strip().lower())
    return ALIASES.get(raw, raw)


def get_retry_variant(
    current_variant: str | None,
    *,
    succeeded: bool,
    available_variants: Sequence[object],
) -> str | None:
    """Select an adjacent difficulty variant without inventing content."""
    current = normalise_variant(current_variant)
    available = []
    seen: set[str] = set()
    for value in available_variants:
        variant = normalise_variant(value)
        if variant and variant not in seen:
            seen.add(variant)
            available.append(variant)

    if not current or current not in DIFFICULTY or not available:
        return None

    current_level = DIFFICULTY[current]
    candidates = [
        variant
        for variant in available
        if variant != current
        and (
            (not succeeded and DIFFICULTY.get(variant, current_level) < current_level)
            or (succeeded and DIFFICULTY.get(variant, current_level) > current_level)
        )
    ]
    if not candidates:
        return None

    target_level = current_level - 1 if not succeeded else current_level + 1
    candidates.sort(
        key=lambda variant: (
            abs(DIFFICULTY.get(variant, target_level) - target_level),
            variant,
        )
    )
    return candidates[0]
