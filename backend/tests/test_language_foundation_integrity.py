"""Structural integrity checks for registered language foundation modules."""

from __future__ import annotations

import importlib

import pytest

from app.data import curriculum as curriculum_dispatcher


def _public_ids(items: object, attribute: str = "id") -> set[str]:
    if not isinstance(items, (list, tuple)):
        return set()
    return {
        getattr(item, attribute)
        for item in items
        if getattr(item, attribute, None)
    }


def test_registered_foundations_import_and_expose_curriculum():
    failures: list[str] = []

    for language, module_name in curriculum_dispatcher._LANG_MODULES.items():
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:  # pragma: no cover - failure detail is asserted below
            failures.append(f"{language}: import failed: {exc}")
            continue

        curriculum = getattr(module, "CURRICULUM", None)
        if not isinstance(curriculum, dict) or not curriculum:
            failures.append(f"{language}: missing/empty CURRICULUM")
            continue

        for level in curriculum_dispatcher.CEFR_LEVELS:
            units = curriculum.get(level, [])
            if not units:
                failures.append(f"{language}: {level} has no curriculum units")

    assert not failures, "\n".join(failures)


def test_registered_foundations_have_no_dangling_unit_references():
    failures: list[str] = []

    for language, module_name in curriculum_dispatcher._LANG_MODULES.items():
        module = importlib.import_module(module_name)
        grammar_ids = _public_ids(getattr(module, "GRAMMAR_TOPICS", []))
        vocabulary_ids = _public_ids(getattr(module, "VOCABULARY_SETS", []))

        for level, units in getattr(module, "CURRICULUM", {}).items():
            unit_ids: set[str] = set()
            for unit in units:
                if unit.id in unit_ids:
                    failures.append(f"{language}: duplicate unit id {unit.id}")
                unit_ids.add(unit.id)

                missing_grammar = set(unit.grammar_points) - grammar_ids
                if missing_grammar:
                    failures.append(
                        f"{language}/{level}/{unit.id}: missing grammar {sorted(missing_grammar)}"
                    )

                missing_vocab = set(unit.vocabulary_set_ids) - vocabulary_ids
                if missing_vocab:
                    failures.append(
                        f"{language}/{level}/{unit.id}: missing vocabulary {sorted(missing_vocab)}"
                    )

                if not unit.lesson_types:
                    failures.append(f"{language}/{level}/{unit.id}: no lesson types")
                if not unit.competency_checklist:
                    failures.append(f"{language}/{level}/{unit.id}: no competency checklist")

    assert not failures, "\n".join(failures)


def test_registered_foundations_have_valid_assessments():
    failures: list[str] = []

    for language, module_name in curriculum_dispatcher._LANG_MODULES.items():
        module = importlib.import_module(module_name)
        for question in getattr(module, "ASSESSMENT_BANK", []):
            if len(question.options) != 4:
                failures.append(f"{language}/{question.id}: expected exactly 4 options")
            if question.correct not in question.options:
                failures.append(f"{language}/{question.id}: correct answer is not an option")
            if question.difficulty not in curriculum_dispatcher.CEFR_LEVELS:
                failures.append(f"{language}/{question.id}: invalid difficulty {question.difficulty}")

    assert not failures, "\n".join(failures)


def test_registered_foundations_have_unique_vocabulary_ids():
    failures: list[str] = []

    for language, module_name in curriculum_dispatcher._LANG_MODULES.items():
        module = importlib.import_module(module_name)
        vocabulary = getattr(module, "VOCABULARY_SETS", [])
        ids = [item.id for item in vocabulary if getattr(item, "id", None)]
        duplicates = sorted({item_id for item_id in ids if ids.count(item_id) > 1})
        if duplicates:
            failures.append(f"{language}: duplicate vocabulary ids {duplicates}")

    assert not failures, "\n".join(failures)
