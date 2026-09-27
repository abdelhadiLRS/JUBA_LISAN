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



def test_b1_vocabulary_entries_match_shared_schema():
    """Authored B1 vocabulary must use valid parts of speech and learner-ready text."""
    from app.data.en_GB.vocabulary_b1 import B1_SETS
    allowed = {"noun", "verb", "adjective", "adverb", "phrase", "conjunction", "preposition", "numeral", "pronoun"}

    assert B1_SETS
    for vocab_set in B1_SETS:
        assert vocab_set.level == "B1"
        assert vocab_set.words
        for entry in vocab_set.words:
            assert entry.pos in allowed, f"{vocab_set.id}: {entry.word} -> {entry.pos}"
            assert entry.definition.strip(), f"{vocab_set.id}: missing definition for {entry.word}"
            assert entry.example.strip(), f"{vocab_set.id}: missing example for {entry.word}"

def test_b2_vocabulary_entries_match_shared_schema():
    """Authored B2 vocabulary must use valid parts of speech and learner-ready text."""
    from app.data.en_GB.vocabulary_b2 import B2_SETS

    allowed = {"noun", "verb", "adjective", "adverb", "phrase", "conjunction", "preposition", "numeral", "pronoun"}

    assert B2_SETS
    for vocab_set in B2_SETS:
        assert vocab_set.level == "B2"
        assert vocab_set.words
        for entry in vocab_set.words:
            assert entry.pos in allowed, f"{vocab_set.id}: {entry.word} -> {entry.pos}"
            assert entry.definition.strip(), f"{vocab_set.id}: missing definition for {entry.word}"
            assert entry.example.strip(), f"{vocab_set.id}: missing example for {entry.word}"

def test_c1_vocabulary_entries_match_shared_schema():
    """Authored C1 vocabulary must use valid parts of speech and learner-ready text."""
    from app.data.en_GB.vocabulary_c1 import C1_SETS

    allowed = {"noun", "verb", "adjective", "adverb", "phrase", "conjunction", "preposition", "numeral", "pronoun"}

    assert C1_SETS
    for vocab_set in C1_SETS:
        assert vocab_set.level == "C1"
        assert vocab_set.words
        for entry in vocab_set.words:
            assert entry.pos in allowed, f"{vocab_set.id}: {entry.word} -> {entry.pos}"
            assert entry.definition.strip(), f"{vocab_set.id}: missing definition for {entry.word}"
            assert entry.example.strip(), f"{vocab_set.id}: missing example for {entry.word}"

def test_en_gb_c1_vocabulary_uses_british_spelling():
    """C1 English content must stay consistent with the en_GB locale."""
    from app.data.en_GB.vocabulary_c1 import C1_SETS

    text = "\\n".join(
        f"{entry.word} {entry.definition} {entry.example}"
        for vocabulary_set in C1_SETS
        for entry in vocabulary_set.words
    ).casefold()

    american_to_british = {
        "galvanize": "galvanise",
        "scrutinize": "scrutinise",
        "organization": "organisation",
        "favor": "favour",
        "skeptical": "sceptical",
    }

    for american, british in american_to_british.items():
        assert american not in text, f"American spelling remains in C1 content: {american}"
        assert british in text, f"Expected British spelling is missing from C1 content: {british}"


def test_c2_vocabulary_entries_match_shared_schema():
    """Authored C2 vocabulary must use valid parts of speech and learner-ready text."""
    from app.data.en_GB.vocabulary_c2 import C2_SETS

    allowed = {"noun", "verb", "adjective", "adverb", "phrase", "conjunction", "preposition", "numeral", "pronoun"}

    assert C2_SETS
    for vocab_set in C2_SETS:
        assert vocab_set.level == "C2"
        assert vocab_set.words
        for entry in vocab_set.words:
            assert entry.pos in allowed, f"{vocab_set.id}: {entry.word} -> {entry.pos}"
            assert entry.definition.strip(), f"{vocab_set.id}: missing definition for {entry.word}"
            assert entry.example.strip(), f"{vocab_set.id}: missing example for {entry.word}"

def test_en_gb_vocabulary_has_no_exact_duplicate_entries_across_cefr_levels():
    """Do not silently teach the identical word/POS/definition at multiple levels."""
    from app.data.en_GB.vocabulary import VOCABULARY_SETS

    seen: dict[tuple[str, str, str], str] = {}
    duplicates: list[tuple[str, str]] = []

    for vocabulary_set in VOCABULARY_SETS:
        for entry in vocabulary_set.words:
            key = (
                entry.word.strip().casefold(),
                entry.pos.strip().casefold(),
                entry.definition.strip(),
            )
            previous_level = seen.get(key)
            if previous_level is not None and previous_level != vocabulary_set.level:
                duplicates.append((entry.word, f"{previous_level}/{vocabulary_set.level}"))
            elif previous_level is None:
                seen[key] = vocabulary_set.level

    assert not duplicates, (
        "Exact vocabulary duplicates were found across CEFR levels: "
        + ", ".join(f"{word} ({levels})" for word, levels in duplicates)
    )


def test_en_gb_vocabulary_has_no_exact_duplicate_entries_within_level():
    """Do not duplicate the same word/POS/definition inside a CEFR level."""
    from app.data.en_GB.vocabulary import VOCABULARY_SETS

    seen: set[tuple[str, str, str, str]] = set()
    duplicates: list[str] = []

    for vocabulary_set in VOCABULARY_SETS:
        for entry in vocabulary_set.words:
            key = (
                vocabulary_set.level,
                entry.word.strip().casefold(),
                entry.pos.strip().casefold(),
                entry.definition.strip(),
            )
            if key in seen:
                duplicates.append(f"{vocabulary_set.level}: {entry.word}")
            else:
                seen.add(key)

    assert not duplicates, "Exact within-level duplicates: " + ", ".join(duplicates)
\n


def test_en_gb_c2_examples_show_advanced_usage_in_context():
    """Selected C2 examples should demonstrate natural collocations and useful context."""
    from app.data.en_GB.vocabulary_c2 import C2_SETS

    entries = [entry for vocab_set in C2_SETS for entry in vocab_set.words]
    examples = {entry.word: entry.example for entry in entries}
    expected_contexts = {
        "elusive": "a reliable solution remained elusive",
        "nascent": "with cautious optimism",
        "commensurate": "experience and responsibilities",
        "token gesture": "working conditions remained unchanged",
        "shed light on": "root causes of staff turnover",
        "obfuscate": "instead of clarifying them",
    }
    for word, phrase in expected_contexts.items():
        assert phrase.casefold() in examples[word].casefold()


def test_en_gb_c1_examples_are_contextual_and_reusable():
    """C1 examples should teach natural usage, not merely restate definitions."""
    from app.data.en_GB.vocabulary_c1 import C1_SETS

    entries = [entry for vocab_set in C1_SETS for entry in vocab_set.words]
    assert entries

    for entry in entries:
        assert entry.example.strip()
        assert entry.example.strip().endswith((".", "!", "?"))
        assert entry.example.strip().casefold() != entry.definition.strip().casefold()
        assert len(entry.example.split()) >= 5

    expected_contexts = {
        "articulate": "concerns clearly during the meeting",
        "substantiate": "with sufficient evidence",
        "delineate": "responsibilities of each department",
        "elucidate": "relationship between the two processes",
        "rebut": "presenting new evidence",
    }
    examples = {entry.word: entry.example for entry in entries}
    for word, phrase in expected_contexts.items():
        assert phrase.casefold() in examples[word].casefold()

def test_c1_formal_writing_prioritises_high_utility_language():
    """C1 formal writing should favour broadly useful formal language over archaic legalese."""
    from app.data.en_GB.vocabulary_c1 import C1_SETS

    formal = next(v for v in C1_SETS if v.id == "formal_writing_c1")
    words = {entry.word.casefold() for entry in formal.words}

    for word in {"hitherto", "inasmuch as", "thereof", "aforesaid", "pursuant to", "hereby", "thereafter"}:
        assert word not in words
    for word in {"subsequently", "subject to", "consequently", "prior to", "in response to", "with effect from", "in line with"}:
        assert word in words


def test_c1_idioms_avoid_redundant_fence_variants():
    """Keep one high-utility expression for indecision rather than teaching near-duplicates."""
    from app.data.en_GB.vocabulary_c1 import C1_SETS

    idioms = next(v for v in C1_SETS if v.id == "idioms_c1")
    words = {entry.word.casefold() for entry in idioms.words}
    assert "on the fence" in words
    assert "sit on the fence" not in words

def test_en_gb_c2_definitions_distinguish_precise_meanings():
    """Selected C2 definitions should explain semantic nuance rather than repeat the headword."""
    from app.data.en_GB.vocabulary_c2 import C2_SETS

    entries = {entry.word: entry for vocab_set in C2_SETS for entry in vocab_set.words}
    expected_definitions = {
        "judicious": "weighing the likely consequences",
        "inextricable": "cannot be separated without changing or losing their meaning",
        "contentious": "provoke strong disagreement or argument",
        "ubiquitous": "seemingly impossible to avoid",
        "ramification": "complex or far-reaching consequences",
        "promulgate": "put a law, rule, or policy into effect",
    }
    for word, phrase in expected_definitions.items():
        assert phrase.casefold() in entries[word].definition.casefold()

def test_en_gb_c2_avoids_redundant_c1_headwords():
    """C2 should not re-teach C1 headwords when the C2 entry adds no distinct meaning."""
    from app.data.en_GB.vocabulary_c1 import C1_SETS
    from app.data.en_GB.vocabulary_c2 import C2_SETS

    c1_headwords = {entry.word.strip().casefold() for vocab_set in C1_SETS for entry in vocab_set.words}
    c2_headwords = {entry.word.strip().casefold() for vocab_set in C2_SETS for entry in vocab_set.words}

    redundant = {"articulate", "notwithstanding", "corroborate", "rhetoric"}
    assert not redundant & c2_headwords
    assert redundant <= c1_headwords
    assert "extrapolate" not in c1_headwords



def test_en_gb_c1_c2_examples_demonstrate_advanced_semantic_use():
    """Selected C1/C2 examples should teach collocation, nuance, and analytical context."""
    from app.data.en_GB.vocabulary_c1 import C1_SETS
    from app.data.en_GB.vocabulary_c2 import C2_SETS

    c1 = {entry.word: entry for vocab_set in C1_SETS for entry in vocab_set.words}
    c2 = {entry.word: entry for vocab_set in C2_SETS for entry in vocab_set.words}

    assert "regulator's authority" in c1["ambiguity"].example
    assert "management paradigm" in c1["paradigm"].example
    assert "fragile consensus" in c1["consensus"].example
    assert "licensing requirements" in c1["circumvent"].example
    assert "community clinics" in c1["alleviate"].example

    assert "certainty is possible" in c2["epistemology"].example
    assert "ontological assumptions" in c2["ontology"].example
    assert "socially neutral" in c2["hegemony"].example
    assert "precedence over equity" in c2["interrogate"].example
    assert "reproduced through institutions" in c2["posit"].example
    assert "climate resilience" in c2["discourse"].example
    assert "social and economic constraints" in c2["reductionism"].example
    assert "stronger evidence emerges" in c2["tenet"].example

def test_en_gb_c2_has_no_duplicate_headword_and_part_of_speech():
    """Avoid teaching the same C2 headword twice with the same grammatical role."""
    from app.data.en_GB.vocabulary_c2 import C2_SETS

    seen: dict[tuple[str, str], str] = {}
    duplicates: list[str] = []
    for vocabulary_set in C2_SETS:
        for entry in vocabulary_set.words:
            key = (entry.word.strip().casefold(), entry.pos.strip().casefold())
            previous_set = seen.get(key)
            if previous_set is not None:
                duplicates.append(f"{entry.word} ({previous_set}/{vocabulary_set.id})")
            else:
                seen[key] = vocabulary_set.id

    assert not duplicates, "Duplicate C2 headwords: " + ", ".join(duplicates)


def test_en_gb_c1_core_examples_teach_collocations_and_real_context():
    """Selected C1 examples should expose useful collocations and realistic contexts."""
    from app.data.en_GB.vocabulary_c1 import C1_SETS

    entries = {entry.word: entry for vocab_set in C1_SETS for entry in vocab_set.words}
    expected_contexts = {
        "resilience": "essential services within weeks of the flood",
        "scrutiny": "regulatory scrutiny",
        "magnitude": "magnitude of the housing shortage",
        "precedent": "set a precedent",
        "conundrum": "limited infrastructure",
        "impetus": "fresh impetus",
        "exacerbate": "financial pressure on smaller firms",
        "encompass": "long-term sustainability",
        "mitigate": "risk of delays",
        "perpetuate": "perpetuate misconceptions",
        "disseminate": "open-access report",
        "instigate": "procurement process",
    }
    for word, phrase in expected_contexts.items():
        assert phrase.casefold() in entries[word].example.casefold()
