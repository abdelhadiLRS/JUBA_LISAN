"""Tests for language-grounded lesson source material."""

from app.services.lesson_generator import _build_curated_source_material


ACTIVATED = (
    "de-DE", "en-GB", "en-US", "es-ES", "fr-FR", "it-IT", "ja-JP", "ko-KR",
    "pt-PT", "zh-CN", "ar", "ru-RU", "nl-NL", "pl-PL", "da-DK", "el-GR",
    "sv-SE", "no-NO", "fi-FI", "cs-CZ",
)


def test_curated_source_material_is_language_specific_for_all_activated_languages():
    for language in ACTIVATED:
        material = _build_curated_source_material(
            target_language=language,
            cefr_level="A1",
            grammar_points=None,
            vocabulary_set_ids=None,
            topic="everyday communication",
        )
        assert material["target_language"] == language
        assert material["cefr_level"] == "A1"
        assert material["grammar"], language
        assert material["vocabulary"], language
        assert material["phrasebook"], language
        assert material["assessment_examples"], language
        assert all(item["examples"] for item in material["grammar"] if item["examples"] is not None)
        assert all(item["words"] for item in material["vocabulary"])
        assert all(item["phrases"] for item in material["phrasebook"])


def test_curated_source_material_respects_requested_curriculum_refs():
    material = _build_curated_source_material(
        target_language="de-DE",
        cefr_level="A1",
        grammar_points=["verb-sein"],
        vocabulary_set_ids=["begruessung_de_a1"],
        topic="Sich vorstellen und begrüßen",
    )
    assert [item["slug"] for item in material["grammar"]] == ["verb-sein"]
    assert [item["id"] for item in material["vocabulary"]] == ["begruessung_de_a1"]


def test_curated_source_material_supports_non_latin_scripts():
    for language in ("ar", "ja-JP", "ko-KR", "zh-CN", "ru-RU"):
        material = _build_curated_source_material(
            target_language=language,
            cefr_level="A1",
            grammar_points=None,
            vocabulary_set_ids=None,
            topic="greetings",
        )
        words = [word["word"] for entry in material["vocabulary"] for word in entry["words"]]
        assert any(word.strip() for word in words), language
