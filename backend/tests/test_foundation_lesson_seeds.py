from app.services.foundation_lesson_seeds import get_foundation_lesson_seed


SKILLS = ["grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"]


def test_czech_foundation_runtime_seeds_cover_a2_to_c2():
    for level in ["A2", "B1", "B2", "C1", "C2"]:
        unit = f"cs-{level.lower()}-1"
        for skill in SKILLS:
            seed = get_foundation_lesson_seed("cs", level, unit, skill)
            assert seed is not None
            assert seed["title"]
            assert seed["objective"]
            assert seed["source"] in {"language_foundation", "curated_czech"}

            if skill == "reading":
                assert seed.get("text")
                assert len(seed.get("questions", [])) >= 3
            elif skill == "listening":
                assert seed.get("transcript")
            elif skill in {"speaking", "writing"}:
                assert seed.get("prompt")
            elif skill == "vocabulary":
                assert seed.get("words")


def test_unknown_foundation_language_returns_none():
    assert get_foundation_lesson_seed("xx", "B1", "xx-b1-1", "reading") is None


def test_curated_language_is_auto_discovered():
    seed = get_foundation_lesson_seed("no", "C2", "no-c2-unit-8", "speaking")
    assert seed is not None
    assert seed["source"] == "curated_norwegian"
    assert seed["prompt"]


CURATED_LANGUAGES = [
    "tr", "nl", "ru", "pl", "de", "fr", "es", "it", "pt",
    "ja", "ko", "zh", "ro", "cs", "el", "hu", "uk", "fi",
    "sv", "da", "no", "is", "vi", "bg", "sr", "hr", "he",
]


def test_curated_languages_auto_discover_all_core_skills():
    for language in CURATED_LANGUAGES:
        for level in ["A2", "B1", "B2", "C1", "C2"]:
            unit = f"{language}-{level.lower()}-unit-1"
            for skill in SKILLS:
                seed = get_foundation_lesson_seed(language, level, unit, skill)
                assert seed is not None, (language, level, skill)
                assert seed["title"], (language, level, skill)
                assert seed["objective"], (language, level, skill)
                assert seed["source"].startswith("curated_"), (language, level, skill)
                if skill == "reading":
                    assert seed.get("text"), (language, level, skill)
                    assert len(seed.get("questions", [])) >= 3, (language, level, skill)
                elif skill == "listening":
                    assert seed.get("transcript"), (language, level, skill)
                elif skill in {"speaking", "writing"}:
                    assert seed.get("prompt"), (language, level, skill)
                elif skill == "vocabulary":
                    assert seed.get("words"), (language, level, skill)


def test_curated_language_curriculum_units_match_runtime_seed_keys():
    from app.data.curriculum import get_curriculum

    for language in CURATED_LANGUAGES:
        curriculum = get_curriculum(language)
        for level in ["A2", "B1", "B2", "C1", "C2"]:
            units = curriculum.get(level, [])
            assert units, (language, level)
            for unit in units:
                assert unit.lesson_types, (language, level, unit.id)
                for skill in unit.lesson_types:
                    seed = get_foundation_lesson_seed(language, level, unit.id, skill)
                    assert seed is not None, (language, level, unit.id, skill)
                    assert seed.get("unit_id") == unit.id, (language, level, unit.id, skill)


def test_foundation_seed_exposes_pedagogical_quality_contract():
    seed = get_foundation_lesson_seed("en_GB", "A1", "a1-unit-1", "speaking")
    assert seed is not None
    assert seed["can_do"]
    assert len(seed["success_criteria"]) >= 2
    assert seed["scenario"]
    assert seed["retrieval_prompts"]
    assert seed["recycle"]
    assert seed["phrases"]


def test_curriculum_units_provide_four_skill_practice_and_competencies():
    """Every CEFR unit should support the four core skills, not grammar-only study."""
    from app.data.curriculum import CEFR_LEVELS, get_curriculum

    for level in CEFR_LEVELS:
        units = get_curriculum("en-GB")[level]
        assert units, level
        for unit in units:
            assert unit.competency_checklist, unit.id
            assert {"reading", "listening", "speaking", "writing"} <= set(unit.lesson_types), unit.id


def test_a1_vocabulary_uses_only_supported_parts_of_speech():
    """Authored A1 entries must conform to the shared vocabulary schema."""
    from app.data.en_GB.vocabulary import VOCABULARY_SETS
    allowed = {"noun", "verb", "adjective", "adverb", "phrase", "conjunction", "preposition", "numeral", "pronoun"}

    for vocab_set in VOCABULARY_SETS:
        for entry in vocab_set.words:
            assert entry.pos in allowed, f"{vocab_set.id}: {entry.word} -> {entry.pos}"



def test_a2_vocabulary_entries_match_shared_schema():
    """Authored A2 vocabulary must use valid parts of speech and usable teaching text."""
    from app.data.en_GB.vocabulary_a2 import A2_SETS
    allowed = {"noun", "verb", "adjective", "adverb", "phrase", "conjunction", "preposition", "numeral", "pronoun"}

    assert A2_SETS
    for vocab_set in A2_SETS:
        assert vocab_set.level == "A2"
        assert vocab_set.words
        for entry in vocab_set.words:
            assert entry.pos in allowed, f"{vocab_set.id}: {entry.word} -> {entry.pos}"
            assert entry.definition.strip(), f"{vocab_set.id}: missing definition for {entry.word}"
            assert entry.example.strip(), f"{vocab_set.id}: missing example for {entry.word}"
