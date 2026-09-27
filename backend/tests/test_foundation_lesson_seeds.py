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



def test_en_gb_b1_core_examples_are_contextual_and_reusable():
    """Selected B1 examples should teach everyday meaning through specific, reusable contexts."""
    from app.data.en_GB.vocabulary_b1 import B1_SETS

    entries = {entry.word: entry for vocab_set in B1_SETS for entry in vocab_set.words}
    expected_contexts = {
        "experience": "international team",
        "achievement": "working full-time",
        "challenge": "affordable accommodation",
        "opportunity": "practical experience",
        "benefit": "better sleep",
        "manage": "before the deadline",
        "improve": "reviewing the difficult sounds",
        "succeed": "local demand",
        "device": "home visits",
        "software": "payment is overdue",
        "download": "without an internet connection",
        "upload": "application is reviewed",
        "search": "entry requirements",
        "update": "critical fix",
        "sustainable": "reduce emissions",
        "recycle": "packaging separately",
        "consequence": "rely on public transport",
        "outcome": "pilot period",
        "consider": "cancellation terms",
        "affect": "customer confidence",
    }
    for word, phrase in expected_contexts.items():
        assert phrase.casefold() in entries[word].example.casefold()
        assert len(entries[word].example.split()) >= 8


def test_en_gb_b2_core_examples_teach_contextual_collocations():
    """Selected B2 examples should model useful professional and analytical contexts."""
    from app.data.en_GB.vocabulary_b2 import B2_SETS

    entries = {entry.word: entry for vocab_set in B2_SETS for entry in vocab_set.words}
    expected_contexts = {
        "analyse": "exposed to rising energy costs",
        "conclude": "cost projections and staffing requirements",
        "demonstrate": "shorter procurement cycles",
        "evaluate": "original criteria",
        "justify": "evidence available at the time",
        "significant": "customer retention",
        "assumption": "demand will remain stable",
        "implication": "small suppliers",
        "stakeholder": "timetable for construction",
        "transparent": "how each charge is calculated",
        "implement": "staff training and revised reporting procedures",
        "objective": "reduce processing times",
        "subsequently": "leading a successful audit",
        "prior to": "supporting documentation",
        "consequently": "termination clause",
    }
    for word, phrase in expected_contexts.items():
        assert phrase.casefold() in entries[word].example.casefold()


def test_en_gb_b2_has_no_duplicate_headword_and_part_of_speech():
    """B2 vocabulary should not repeat the same headword/POS pair."""
    from app.data.en_GB.vocabulary_b2 import B2_SETS

    seen = set()
    for vocab_set in B2_SETS:
        for entry in vocab_set.words:
            key = (entry.word.casefold(), entry.pos.casefold())
            assert key not in seen, f"Duplicate B2 vocabulary entry: {entry.word} ({entry.pos})"
            seen.add(key)


def test_en_gb_c1_overlaps_with_b2_add_semantic_or_register_value():
    """Intentional B2/C1 overlaps should teach a materially more specific C1 use."""
    from app.data.en_GB.vocabulary_b2 import B2_SETS
    from app.data.en_GB.vocabulary_c1 import C1_SETS

    b2 = {entry.word: entry for vocab_set in B2_SETS for entry in vocab_set.words}
    c1 = {entry.word: entry for vocab_set in C1_SETS for entry in vocab_set.words}

    assert "confirmation bias" not in b2["bias"].example.casefold()
    assert "selection bias" in c1["bias"].example.casefold()
    assert "directly comparable" not in b2["implication"].example.casefold()
    assert "directly comparable" in c1["implication"].example.casefold()


def test_en_gb_c2_empirical_example_adds_methodological_nuance():
    """C2 empirical usage should move beyond the general B2 meaning into research methodology."""
    from app.data.en_GB.vocabulary_b2 import B2_SETS
    from app.data.en_GB.vocabulary_c2 import C2_SETS

    b2 = {entry.word: entry for vocab_set in B2_SETS for entry in vocab_set.words}
    c2 = {entry.word: entry for vocab_set in C2_SETS for entry in vocab_set.words}

    assert "empirical evidence" in b2["empirical"].example.casefold()
    assert "controlled studies" in c2["empirical"].example.casefold()
    assert "theoretical claim" in c2["empirical"].definition.casefold()


def test_en_gb_c2_core_examples_teach_advanced_collocations():
    """Selected C2 examples should teach domain-specific collocations and nuanced usage."""
    from app.data.en_GB.vocabulary_c2 import C2_SETS

    entries = {entry.word: entry for vocab_set in C2_SETS for entry in vocab_set.words}
    expected_contexts = {
        "seminal": "reshaped subsequent linguistic research",
        "convoluted": "applicable requirements",
        "tenuous": "fall in exports",
        "judicious": "allocation of research funding",
        "ubiquitous": "urban commerce",
        "esoteric": "early analytic philosophy",
        "pervasive": "disclosure was voluntary",
        "discerning": "repackages familiar claims",
        "pertinent": "reduce competition",
        "heretofore": "accepted account of the negotiations",
        "subsume": "single compliance process",
    }
    for word, phrase in expected_contexts.items():
        assert phrase.casefold() in entries[word].example.casefold()


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
    for word in {"accordingly", "subject to", "thereby", "in response to", "with effect from", "in line with", "insofar as"}:
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


def test_en_gb_b2_overlap_examples_add_specific_context():
    """Intentional B1/B2 overlaps should add domain, precision, or decision-making value at B2."""
    from app.data.en_GB.vocabulary_b1 import B1_SETS
    from app.data.en_GB.vocabulary_b2 import B2_SETS

    b1 = {entry.word: entry for vocab_set in B1_SETS for entry in vocab_set.words}
    b2 = {entry.word: entry for vocab_set in B2_SETS for entry in vocab_set.words}

    expected_contexts = {
        "alternative": "stronger technical support",
        "coverage": "national newspapers",
        "efficient": "duplicate data entry",
        "evidence": "supplier’s explanation",
        "manufacture": "highly automated production lines",
        "meanwhile": "temporary production elsewhere",
        "outcome": "decide whether to expand the service",
        "renewable": "long-term operating emissions",
        "sustainable": "expense of accessibility",
        "regret": "final testing phase",
    }
    for word, phrase in expected_contexts.items():
        assert word in b1 and word in b2
        assert phrase.casefold() in b2[word].example.casefold()
        assert b2[word].example.casefold() != b1[word].example.casefold()
        assert len(b2[word].example.split()) >= 10


def test_en_gb_b2_core_examples_are_contextual_and_reusable():
    """Selected B2 examples should teach reusable collocations in realistic contexts."""
    from app.data.en_GB.vocabulary_b2 import B2_SETS

    entries = {entry.word: entry for vocabulary_set in B2_SETS for entry in vocabulary_set.words}
    expected_contexts = {
        "criterion": "after-sales support",
        "hypothesis": "shorter delivery times",
        "perspective": "customer perspective",
        "relevant": "decision under consideration",
        "consistent": "regional offices",
        "colleague": "monthly accounts",
        "negotiate": "production delay",
        "collaborate": "safer use in hospitals",
        "priorities": "deadline changed",
        "feedback": "abandoned transactions",
        "budget": "energy costs",
        "delegate": "regulatory review",
        "initiative": "alternative suppliers",
        "influence": "investment decisions",
        "bias": "selection process",
        "controversy": "local traffic",
        "campaign": "essential food and clothing",
        "stereotype": "older customers",
        "diversity": "professional backgrounds",
        "inequality": "specialist healthcare",
        "journalism": "could not initially be verified",
        "globalisation": "several countries",
        "mainstream": "ordinary workplace software",
        "sensationalise": "unverified claims",
        "accountability": "who approved each stage",
        "in retrospect": "backup system",
        "predecessor": "easier to maintain",
        "simultaneously": "update inventory",
        "allegation": "disputed transaction",
        "dispute": "contractual dispute",
        "summit": "industrial emissions",
        "treaty": "shared rules",
        "coalition": "local businesses and residents",
        "eyewitness": "accounts of the collision",
        "speculation": "cause of the outage",
        "breakthrough": "cheaper to manufacture",
        "phenomenon": "different climates",
        "theoretical": "case studies",
        "evaluation": "independent evaluation",
    }
    for word, phrase in expected_contexts.items():
        assert phrase.casefold() in entries[word].example.casefold()
        assert len(entries[word].example.split()) >= 10


def test_en_gb_b2_c1_overlaps_add_semantic_or_domain_value():
    """Intentional B2/C1 overlaps should become more precise or more specialised at C1."""
    from app.data.en_GB.vocabulary_b2 import B2_SETS
    from app.data.en_GB.vocabulary_c1 import C1_SETS

    b2 = {entry.word: entry for vocab_set in B2_SETS for entry in vocab_set.words}
    c1 = {entry.word: entry for vocab_set in C1_SETS for entry in vocab_set.words}

    expected = {
        "implication": "revised sampling method",
        "bias": "selection bias",
    }
    for word, phrase in expected.items():
        assert word in b2 and word in c1
        assert phrase.casefold() in c1[word].example.casefold()
        assert c1[word].example.casefold() != b2[word].example.casefold()
        assert len(c1[word].example.split()) >= 12

    assert "inference" in c1["implication"].definition.casefold()
    assert "systematic tendency" in c1["bias"].definition.casefold()


def test_en_gb_progression_overlaps_add_level_appropriate_value():
    """Selected overlaps should gain precision, context, or abstraction at the next CEFR level."""
    from app.data.en_GB.vocabulary_a2 import A2_SETS
    from app.data.en_GB.vocabulary_b1 import B1_SETS
    from app.data.en_GB.vocabulary_c1 import C1_SETS
    from app.data.en_GB.vocabulary_c2 import C2_SETS

    a2 = {entry.word: entry for vocab_set in A2_SETS for entry in vocab_set.words}
    b1 = {entry.word: entry for vocab_set in B1_SETS for entry in vocab_set.words}
    c1 = {entry.word: entry for vocab_set in C1_SETS for entry in vocab_set.words}
    c2 = {entry.word: entry for vocab_set in C2_SETS for entry in vocab_set.words}

    expected = {
        "A2": {
            "tall": "tallest person",
            "beautiful": "especially in spring",
            "head": "hit his head lightly",
            "arm": "wear a support",
            "leg": "stopped running",
        },
        "B1": {
            "meanwhile": "moved their work to another room",
            "worth": "guided tour",
            "species": "natural habitats",
            "habitat": "cleared for agriculture",
        },
        "C2": {
            "ambiguity": "competing interpretations",
            "paradigm": "dominant paradigm",
        },
    }
    for word, phrase in expected["A2"].items():
        assert phrase.casefold() in a2[word].example.casefold()
        assert len(a2[word].example.split()) >= 10
    for word, phrase in expected["B1"].items():
        assert phrase.casefold() in b1[word].example.casefold()
        assert len(b1[word].example.split()) >= 10
    for word, phrase in expected["C2"].items():
        assert phrase.casefold() in c2[word].example.casefold()
        assert len(c2[word].example.split()) >= 12

    assert "contextual analysis" in c1["ambiguity"].definition.casefold()
    assert "intellectual framework" in c2["paradigm"].definition.casefold()
    assert b1["meanwhile"].example.casefold() != a2["meanwhile"].example.casefold()


def test_en_gb_a2_b1_core_examples_are_contextual_and_reusable():
    """Selected A2/B1 examples should teach meaning through realistic situations."""
    from app.data.en_GB.vocabulary_a2 import A2_SETS
    from app.data.en_GB.vocabulary_b1 import B1_SETS

    a2 = {entry.word: entry for vocabulary_set in A2_SETS for entry in vocabulary_set.words}
    b1 = {entry.word: entry for vocabulary_set in B1_SETS for entry in vocabulary_set.words}

    a2_contexts = {
        "suddenly": "lights went out",
        "immediately": "called a taxi",
        "at first": "new timetable confusing",
        "in the end": "least traffic",
        "later": "this afternoon",
        "next": "completed form",
        "after that": "finished the meeting",
        "soon": "checking the connection",
    }
    b1_contexts = {
        "memorable": "whole audience joined",
        "screen": "fell from the desk",
        "honestly": "practical sessions",
        "option": "travel by train",
        "stage": "testing phase",
        "system": "change their appointments",
        "opinion": "more evidence",
        "resemble": "original building",
        "specific": "problem that the new policy",
        "voluntary": "choose whether or not",
    }

    for word, phrase in a2_contexts.items():
        assert phrase.casefold() in a2[word].example.casefold()
        assert len(a2[word].definition.split()) >= 8
        assert len(a2[word].example.split()) >= 10

    for word, phrase in b1_contexts.items():
        assert phrase.casefold() in b1[word].example.casefold()
        assert len(b1[word].definition.split()) >= 8
        assert len(b1[word].example.split()) >= 10


def test_en_gb_a1_identity_and_greetings_are_contextual():
    """Core A1 identity and greeting entries should teach usable language, not isolated definitions."""
    from app.data.en_GB.vocabulary_a1 import A1_SETS

    entries = {entry.word: entry for vocabulary_set in A1_SETS for entry in vocabulary_set.words}
    expected = {
        "name": "friends usually call me",
        "age": "two years younger",
        "city": "small city",
        "teacher": "practise speaking",
        "email": "meeting time and address",
        "address": "full address",
        "profession": "local hospital",
        "married": "have two children",
        "single": "shares a flat",
        "spell": "write it down",
        "introduce": "from Manchester",
        "hello": "new neighbour",
        "goodbye": "colleagues before leaving",
        "please": "open the window",
        "thank you": "carry the boxes",
        "sorry": "bus was delayed",
        "welcome": "our class",
        "nice": "plans for the weekend",
        "meet": "spoken by email",
        "fine": "short rest",
        "evening": "after everyone gets home",
    }
    for word, phrase in expected.items():
        assert phrase.casefold() in entries[word].example.casefold()
        assert len(entries[word].definition.split()) >= 7
        assert len(entries[word].example.split()) >= 7


def test_en_gb_a2_b2_selected_examples_add_teaching_context():
    """Selected entries should explain meaning through concrete, reusable contexts."""
    from app.data.en_GB.vocabulary_a2 import A2_SETS
    from app.data.en_GB.vocabulary_b2 import B2_SETS

    a2 = {entry.word: entry for s in A2_SETS for entry in s.words}
    b2 = {entry.word: entry for s in B2_SETS for entry in s.words}
    expected = {
        "eventually": ("three people", 10),
        "meanwhile": ("customers' questions", 10),
        "hope": ("save enough money", 10),
        "intend": ("cancelled my other appointments", 10),
        "book": ("restaurant", 10),
        "decision": ("better job", 10),
        "traditional": ("local music and food", 10),
        "exciting": ("last ten minutes", 10),
    }
    for word, (phrase, minimum) in expected.items():
        assert phrase.casefold() in a2[word].example.casefold()
        assert len(a2[word].example.split()) >= minimum

    expected_b2 = {
        "variable": "recorded it throughout the trial",
        "censorship": "restricted reporting",
        "circulation": "cheaper weekend edition",
        "preceding": "financial model",
        "ensuing": "asked for more evidence",
        "foreseeable": "changes in demand",
        "unfold": "compared the original documents",
        "remorse": "harm caused to the family",
        "apprehensive": "large organisation",
        "overwhelmed": "first week",
        "melancholy": "lively rhythm",
    }
    for word, phrase in expected_b2.items():
        assert phrase.casefold() in b2[word].example.casefold()
        assert len(b2[word].definition.split()) >= 8
        assert len(b2[word].example.split()) >= 10


def test_foundation_fallback_seed_has_a_complete_learning_sequence():
    """Fallback lessons should connect input, retrieval, and production."""
    from app.services.foundation_lesson_seeds import get_foundation_lesson_seed

    seed = get_foundation_lesson_seed("en_GB", "A1", "unit-1", "speaking")
    assert seed is not None
    quality = seed["content_quality"]
    assert quality["input_examples"]
    assert quality["target_words"]
    assert quality["target_phrases"]
    assert all(phrase in seed["phrases"] for phrase in quality["target_phrases"])
    assert quality["retrieval_sequence"] == [
        "Recall the meaning of three target items without looking.",
        "Use two target items in new sentences.",
        "Complete the final task using the target grammar or skill.",
    ]
    assert "three target words" in quality["production_requirement"]
    assert "follow-up question" in seed["prompt"]


def test_en_gb_a1_assessment_vocabulary_uses_contextual_prompts():
    """Beginner assessment should test vocabulary through usable situations."""
    from app.data.en_GB.assessment_bank import ASSESSMENT_BANK

    questions = {item.id: item for item in ASSESSMENT_BANK}
    expected = {
        "v-a1-001": "opposite of",
        "v-a1-003": "family member",
        "v-a1-004": "weather is clear",
        "v-a1-007": "room where he sleeps",
        "v-a1-009": "wear on her feet",
    }
    for question_id, phrase in expected.items():
        assert phrase.casefold() in questions[question_id].question.casefold()
        assert len(questions[question_id].question.split()) >= 12


def test_en_gb_advanced_vocabulary_assessments_use_context():
    """Higher-level vocabulary items should be assessed in meaningful contexts."""
    from app.data.en_GB.assessment_bank import ASSESSMENT_BANK

    questions = {item.id: item for item in ASSESSMENT_BANK}
    expected = {
        "v-a2-006": "pay electronically",
        "r-b2-006": "safety measures",
        "r-c1-007": "report contained",
        "v-c2-009": "final terms",
    }
    for question_id, phrase in expected.items():
        question = questions[question_id].question
        assert phrase.casefold() in question.casefold()
        assert len(question.split()) >= 12


def test_en_gb_b1_vocabulary_examples_are_contextual_and_reusable():
    from app.data.en_GB.vocabulary_b1 import B1_SETS

    entries = {
        entry.word: entry
        for vocabulary_set in B1_SETS
        for entry in vocabulary_set.words
    }

    expected = {
        "wireless": "hotel provides wireless internet",
        "password": "Change your password regularly",
        "artificial intelligence": "helping hospitals analyse medical images",
        "I think": "because the roads are usually busy",
        "unforgettable": "audience joined the singer",
        "apparently": "venue has a problem with its electrical system",
    }
    for word, phrase in expected.items():
        assert phrase in entries[word].example


def test_en_gb_a2_vocabulary_examples_are_contextual_and_reusable():
    from app.data.en_GB.vocabulary_a2 import A2_SETS

    entries = {
        entry.word: entry
        for vocabulary_set in A2_SETS
        for entry in vocabulary_set.words
    }
    expected = {
        "comfortable": "when I read in the evening",
        "dangerous": "few street lights",
        "popular": "offers cheap tickets",
        "difficult": "asked the teacher for another example",
        "modern": "charging points for visitors",
        "quiet": "after the shops close",
        "crowded": "waited for the next one",
        "village": "less traffic and fewer shops",
        "region": "prepare for frost earlier",
    }
    for word, phrase in expected.items():
        assert phrase in entries[word].example
