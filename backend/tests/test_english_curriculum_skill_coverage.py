"""English curriculum skill coverage tests."""

import importlib

import pytest


LEVELS = ["a2", "b1", "b2", "c1", "c2"]
REQUIRED_SKILLS = {
    "grammar",
    "vocabulary",
    "reading",
    "listening",
    "speaking",
    "writing",
    "review",
}


@pytest.mark.parametrize("locale", ["en_GB", "en_US"])
@pytest.mark.parametrize("level", LEVELS)
def test_every_english_unit_covers_all_seven_skills(locale: str, level: str) -> None:
    module = importlib.import_module(f"app.data.{locale}.curriculum_{level}")
    units = getattr(module, f"{level.upper()}_UNITS")

    assert units, f"{locale} {level.upper()} must define curriculum units"
    for unit in units:
        assert REQUIRED_SKILLS.issubset(set(unit.lesson_types)), (
            f"{locale} {unit.id} is missing skills: "
            f"{sorted(REQUIRED_SKILLS - set(unit.lesson_types))}"
        )
