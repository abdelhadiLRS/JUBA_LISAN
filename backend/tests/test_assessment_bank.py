"""Unit tests for the language-dispatched assessment bank."""

from __future__ import annotations


class TestGetAssessmentBank:
    def test_english_returns_non_empty(self):
        from app.data.assessment_bank import get_assessment_bank

        bank = get_assessment_bank("en-GB")
        assert isinstance(bank, list)
        assert len(bank) > 0

    def test_en_us_returns_non_empty(self):
        from app.data.assessment_bank import get_assessment_bank

        bank = get_assessment_bank("en-US")
        assert isinstance(bank, list)
        assert len(bank) > 0

    def test_spanish_returns_non_empty(self):
        from app.data.assessment_bank import get_assessment_bank

        bank = get_assessment_bank("es-ES")
        assert isinstance(bank, list)
        assert len(bank) > 0

    def test_french_returns_non_empty(self):
        from app.data.assessment_bank import get_assessment_bank

        bank = get_assessment_bank("fr")
        assert isinstance(bank, list)
        assert len(bank) > 0

    def test_german_returns_non_empty(self):
        from app.data.assessment_bank import get_assessment_bank

        bank = get_assessment_bank("de")
        assert isinstance(bank, list)
        assert len(bank) > 0

    def test_italian_returns_non_empty(self):
        from app.data.assessment_bank import get_assessment_bank

        bank = get_assessment_bank("it")
        assert isinstance(bank, list)
        assert len(bank) > 0

    def test_portuguese_returns_non_empty(self):
        from app.data.assessment_bank import get_assessment_bank

        bank = get_assessment_bank("pt")
        assert isinstance(bank, list)
        assert len(bank) > 0

    def test_japanese_returns_non_empty(self):
        from app.data.assessment_bank import get_assessment_bank

        bank = get_assessment_bank("ja-JP")
        assert isinstance(bank, list)
        assert len(bank) > 0
        assert any(q.id == "ja-g-a1-001" for q in bank)

    def test_korean_returns_non_empty(self):
        from app.data.assessment_bank import get_assessment_bank

        bank = get_assessment_bank("ko-KR")
        assert isinstance(bank, list)
        assert len(bank) == 132
        assert any(q.id == "ko-g-a1-001" for q in bank)

    def test_chinese_returns_non_empty(self):
        from app.data.assessment_bank import get_assessment_bank

        bank = get_assessment_bank("zh-CN")
        assert isinstance(bank, list)
        assert len(bank) == 180
        assert any(q.id == "zh-g-a1-001" for q in bank)

    def test_unknown_language_falls_back_to_en_gb(self):
        from app.data.assessment_bank import get_assessment_bank

        bank_unknown = get_assessment_bank("xx-XX")
        bank_gb = get_assessment_bank("en-GB")
        assert bank_unknown == bank_gb

    def test_empty_language_falls_back_to_en_gb(self):
        from app.data.assessment_bank import get_assessment_bank

        bank_empty = get_assessment_bank("")
        bank_gb = get_assessment_bank("en-GB")
        assert bank_empty == bank_gb

    def test_cache_reuses_imported_module(self):
        from app.data.assessment_bank import _CACHE, get_assessment_bank

        _CACHE.clear()
        b1 = get_assessment_bank("en-GB")
        b2 = get_assessment_bank("en-GB")
        assert b1 is b2
        assert len(_CACHE) == 1

    def test_iso_fallback_de_de(self):
        from app.data.assessment_bank import get_assessment_bank

        bank_de_de = get_assessment_bank("de-DE")
        bank_de = get_assessment_bank("de")
        assert bank_de_de == bank_de

    def test_fr_ca_fallback_to_fr(self):
        from app.data.assessment_bank import get_assessment_bank

        bank_fr_ca = get_assessment_bank("fr-CA")
        bank_fr = get_assessment_bank("fr")
        assert bank_fr_ca == bank_fr

    def test_region_variant_accepts_underscore_and_mixed_case(self):
        from app.data.assessment_bank import get_assessment_bank

        canonical = get_assessment_bank("en-US")
        assert get_assessment_bank("en_US") == canonical
        assert get_assessment_bank(" EN-us ") == canonical

    def test_language_tag_normalizer_handles_empty_and_region_tags(self):
        from app.data.assessment_bank import _normalise_language_tag

        assert _normalise_language_tag(None) == "en-GB"
        assert _normalise_language_tag("  ") == "en-GB"
        assert _normalise_language_tag("PT_br") == "pt-BR"
        assert _normalise_language_tag("ZH-hant") == "zh-Hant"


    def test_dutch_assessment_bank_has_balanced_cefr_coverage_and_valid_options(self):
        from app.data.assessment_bank import get_assessment_bank

        bank = get_assessment_bank("nl-NL")
        assert bank
        assert {question.difficulty for question in bank} == {"A1", "A2", "B1", "B2", "C1", "C2"}
        assert len({question.id for question in bank}) == len(bank)
        assert all(len(question.options) == 4 for question in bank)
        assert all(question.correct in question.options for question in bank)
        counts = {
            level: sum(question.difficulty == level for question in bank)
            for level in {question.difficulty for question in bank}
        }
        assert all(count >= 4 for count in counts.values())

    def test_finnish_assessment_bank_has_balanced_cefr_coverage_and_valid_options(self):
        from app.data.assessment_bank import get_assessment_bank

        bank = get_assessment_bank("fi-FI")
        levels = {"A1", "A2", "B1", "B2", "C1", "C2"}
        assert bank
        assert {question.difficulty for question in bank} == levels
        assert len({question.id for question in bank}) == len(bank)
        assert all(len(question.options) == 4 for question in bank)
        assert all(question.correct in question.options for question in bank)
        counts = {
            level: sum(question.difficulty == level for question in bank)
            for level in levels
        }
        assert counts == {level: 12 for level in levels}

    def test_all_registered_assessment_banks_have_unique_nonempty_question_ids():
        from app.data.assessment_bank import _LANG_MODULES, get_assessment_bank

        for language in _LANG_MODULES:
            bank = get_assessment_bank(language)
            ids = [question.id for question in bank]
            assert bank, f"Assessment bank is empty for {language}"
            assert all(isinstance(question_id, str) and question_id.strip() for question_id in ids), (
                f"Assessment bank contains an empty question ID for {language}"
            )
            assert len(ids) == len(set(ids)), f"Duplicate assessment question IDs for {language}"

    def test_all_registered_banks_have_complete_answerable_questions():
        from app.data.assessment_bank import _LANG_MODULES, get_assessment_bank

        valid_levels = {"A1", "A2", "B1", "B2", "C1", "C2"}
        valid_skills = {"grammar", "vocabulary", "reading"}
        for language in _LANG_MODULES:
            for question in get_assessment_bank(language):
                prefix = f"{language}:{question.id}"
                assert question.question.strip(), f"Empty prompt: {prefix}"
                assert question.skill in valid_skills, f"Invalid skill: {prefix}"
                assert question.difficulty in valid_levels, f"Invalid CEFR level: {prefix}"
                assert len(question.options) == 4, f"Expected four options: {prefix}"
                assert all(isinstance(option, str) and option.strip() for option in question.options), (
                    f"Empty answer option: {prefix}"
                )
                assert len({option.strip().casefold() for option in question.options}) == 4, (
                    f"Duplicate answer options: {prefix}"
                )
                assert question.correct in question.options, f"Correct answer missing from options: {prefix}"



    def test_en_gb_b1_to_c2_vocabulary_assessments_use_context(self):
        from app.data.en_GB.assessment_bank import ASSESSMENT_BANK

        expected = {
            "v-a2-001": "After moving from Morocco to Spain",
            "v-a2-007": "annual staff meeting",
            "v-a2-008": "tomorrow’s newspaper",
            "v-a2-009": "starters, main courses, desserts",
            "v-b1-001": "training programme",
            "v-b1-003": "speak in front of the class",
            "v-b1-008": "same office",
            "v-b2-004": "online banking",
            "v-c1-001": "closed the branch",
            "v-c1-003": "effects of misinformation",
            "v-c2-004": "spokesperson equivocated",
        }
        questions = {question.id: question.question for question in ASSESSMENT_BANK}
        for question_id, context in expected.items():
            assert context in questions[question_id]
            assert "What does" not in questions[question_id] or "here" in questions[question_id]


    def test_en_gb_vocabulary_distractors_are_not_duplicate_meanings(self):
        from app.data.en_GB.assessment_bank import ASSESSMENT_BANK

        questions = {question.id: question for question in ASSESSMENT_BANK}
        assert questions["v-b1-001"].options == ["minor", "urgent", "important", "predictable"]
        assert questions["v-b2-002"].options == [
            "open to several interpretations",
            "well-supported by evidence",
            "emotionally charged",
            "unrelated to the topic",
        ]
        assert questions["v-c1-003"].options == [
            "causing lasting harm",
            "providing a useful benefit",
            "causing only temporary inconvenience",
            "improving conditions",
        ]
        for question_id in ("v-b1-001", "v-b2-002", "v-c1-003"):
            question = questions[question_id]
            assert question.correct in question.options
            assert len(set(question.options)) == 4


    def test_en_gb_advanced_vocabulary_prompts_use_realistic_context(self):
        from app.data.en_GB.assessment_bank import ASSESSMENT_BANK

        questions = {question.id: question.question for question in ASSESSMENT_BANK}
        expected = {
            "v-b2-007": "company made substantial progress after six months of testing",
            "v-c1-006": "strict procurement rule",
            "v-c2-008": "contract clause can be read in two different ways",
        }
        for question_id, context in expected.items():
            assert context in questions[question_id]
            assert questions[question_id].strip()
