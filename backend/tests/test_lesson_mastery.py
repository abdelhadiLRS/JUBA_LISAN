from types import SimpleNamespace

from app.schemas.lessons import LessonMasteryResponse
from app.services.adaptive_variants import summarize_adaptive_mastery
from app.services.lesson_mastery import (
    select_next_mastery_candidate,
    summarize_lesson_mastery,
    summarize_skill_mastery,
    select_next_skill_mastery,
)


def test_lesson_mastery_aggregates_states_and_variants():
    exercises = [
        SimpleNamespace(id=1, content_id="alpha"),
        SimpleNamespace(id=2, content_id="beta"),
        SimpleNamespace(id=3, content_id="gamma"),
        SimpleNamespace(id=4, content_id="delta"),
    ]
    attempts = [
        SimpleNamespace(content_id="alpha", variant="a", score=0.8),
        SimpleNamespace(content_id="alpha", variant="b", score=0.8),
        SimpleNamespace(content_id="beta", variant="a", score=0.2),
        SimpleNamespace(content_id="gamma", variant="a", score=0.6),
    ]

    result = summarize_lesson_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
    )

    assert result.mastery_state == "struggling"
    assert result.total_exercises == 4
    assert result.attempted_exercises == 3
    assert result.mastered_exercises == 1
    assert result.learning_exercises == 1
    assert result.struggling_exercises == 1
    assert result.unseen_exercises == 1
    assert result.average_mastery_score == 0.4
    assert result.attempt_rate == 0.75
    assert result.mastery_rate == 0.25
    assert result.covered_variants == 4


def test_lesson_mastery_treats_blank_or_non_string_content_as_unseen():
    exercises = [
        SimpleNamespace(content_id=""),
        SimpleNamespace(content_id=None),
    ]
    attempts = [
        SimpleNamespace(content_id="x", variant="a", score=1.0),
    ]

    result = summarize_lesson_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
    )

    assert result.mastery_state == "unseen"
    assert result.attempted_exercises == 0
    assert result.unseen_exercises == 2
    assert result.average_mastery_score == 0.0
    assert result.attempt_rate == 0.0
    assert result.mastery_rate == 0.0
    assert result.covered_variants == 0


def test_lesson_mastery_rate_is_zero_for_empty_lesson():
    result = summarize_lesson_mastery(
        [],
        [],
        get_content_id=lambda item: item.content_id,
    )

    assert result.mastery_state == "unseen"
    assert result.total_exercises == 0
    assert result.attempted_exercises == 0
    assert result.mastered_exercises == 0
    assert result.average_mastery_score == 0.0
    assert result.attempt_rate == 0.0
    assert result.mastery_rate == 0.0
    assert result.covered_variants == 0


def test_lesson_mastery_state_is_learning_when_attempted_without_struggling():
    exercises = [
        SimpleNamespace(content_id="alpha"),
        SimpleNamespace(content_id="beta"),
    ]
    attempts = [
        SimpleNamespace(content_id="alpha", variant="a", score=0.70),
        SimpleNamespace(content_id="beta", variant="a", score=0.90),
    ]

    result = summarize_lesson_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
    )

    assert result.mastery_state == "learning"


def test_lesson_mastery_state_is_mastered_when_every_exercise_is_mastered():
    exercises = [
        SimpleNamespace(content_id="alpha"),
        SimpleNamespace(content_id="beta"),
    ]
    attempts = [
        SimpleNamespace(content_id="alpha", variant="a", score=0.80),
        SimpleNamespace(content_id="alpha", variant="b", score=0.80),
        SimpleNamespace(content_id="beta", variant="a", score=0.80),
        SimpleNamespace(content_id="beta", variant="b", score=0.80),
    ]

    result = summarize_lesson_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
    )

    assert result.mastery_state == "mastered"


def test_next_mastery_candidate_prioritizes_struggling_then_unseen_then_learning():
    exercises = [
        SimpleNamespace(id=10, content_id="learning"),
        SimpleNamespace(id=20, content_id="unseen"),
        SimpleNamespace(id=30, content_id="struggling"),
        SimpleNamespace(id=40, content_id="mastered"),
    ]
    attempts = [
        SimpleNamespace(content_id="learning", variant="a", score=0.60),
        SimpleNamespace(content_id="struggling", variant="a", score=0.20),
        SimpleNamespace(content_id="mastered", variant="a", score=0.90),
        SimpleNamespace(content_id="mastered", variant="b", score=0.90),
    ]

    result = select_next_mastery_candidate(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_exercise_id=lambda item: item.id,
    )

    assert result is not None
    assert result.exercise is exercises[2]
    assert result.mastery_state == "struggling"
    assert result.mastery_score == 0.2
    assert result.mastery_variants == 1


def test_next_mastery_candidate_uses_lowest_score_within_same_state():
    exercises = [
        SimpleNamespace(id=10, content_id="first"),
        SimpleNamespace(id=20, content_id="second"),
    ]
    attempts = [
        SimpleNamespace(content_id="first", variant="a", score=0.60),
        SimpleNamespace(content_id="second", variant="a", score=0.55),
    ]

    result = select_next_mastery_candidate(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_exercise_id=lambda item: item.id,
    )

    assert result is not None
    assert result.exercise is exercises[1]
    assert result.mastery_state == "learning"
    assert result.mastery_score == 0.55


def test_next_mastery_candidate_returns_none_when_everything_is_mastered():
    exercises = [
        SimpleNamespace(id=1, content_id="alpha"),
        SimpleNamespace(id=2, content_id="beta"),
    ]
    attempts = [
        SimpleNamespace(content_id="alpha", variant="a", score=0.90),
        SimpleNamespace(content_id="alpha", variant="b", score=0.90),
        SimpleNamespace(content_id="beta", variant="a", score=0.80),
        SimpleNamespace(content_id="beta", variant="b", score=0.80),
    ]

    assert select_next_mastery_candidate(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_exercise_id=lambda item: item.id,
    ) is None


def test_mastery_reason_maps_states_to_stable_reasons():
    from app.services.lesson_mastery import mastery_reason

    assert mastery_reason("struggling") == "struggling"
    assert mastery_reason("unseen") == "unseen"
    assert mastery_reason("learning") == "lowest_mastery"
    assert mastery_reason("unknown") == "lowest_mastery"


def test_next_mastery_candidate_breaks_equal_scores_by_exercise_id():
    exercises = [
        SimpleNamespace(id=30, content_id="later"),
        SimpleNamespace(id=10, content_id="earlier"),
    ]
    attempts = [
        SimpleNamespace(content_id="later", variant="a", score=0.60),
        SimpleNamespace(content_id="earlier", variant="a", score=0.60),
    ]

    result = select_next_mastery_candidate(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_exercise_id=lambda item: item.id,
    )

    assert result is not None
    assert result.exercise is exercises[1]
    assert result.mastery_state == "learning"
    assert result.mastery_score == 0.60


def test_adaptive_mastery_boundary_at_struggling_threshold():
    score, state, variants = summarize_adaptive_mastery(
        [SimpleNamespace(content_id="x", variant="a", score=0.49)],
        content_id="x",
    )
    assert score == 0.49
    assert state == "struggling"
    assert variants == 1


def test_adaptive_mastery_boundary_at_learning_threshold():
    score, state, variants = summarize_adaptive_mastery(
        [SimpleNamespace(content_id="x", variant="a", score=0.50)],
        content_id="x",
    )
    assert score == 0.50
    assert state == "learning"
    assert variants == 1


def test_adaptive_mastery_requires_two_distinct_variants_at_required_score():
    score, state, variants = summarize_adaptive_mastery(
        [
            SimpleNamespace(content_id="x", variant="a", score=0.80),
            SimpleNamespace(content_id="x", variant="a", score=0.90),
        ],
        content_id="x",
    )
    assert score == 0.90
    assert state == "learning"
    assert variants == 1


def test_adaptive_mastery_becomes_mastered_with_two_distinct_variants():
    score, state, variants = summarize_adaptive_mastery(
        [
            SimpleNamespace(content_id="x", variant="a", score=0.80),
            SimpleNamespace(content_id="x", variant="b", score=0.80),
        ],
        content_id="x",
    )
    assert score == 0.80
    assert state == "mastered"
    assert variants == 2



def test_adaptive_mastery_normalizes_duplicate_variant_labels_before_counting():
    score, state, variants = summarize_adaptive_mastery(
        [
            SimpleNamespace(content_id="x", variant="A", score=0.70),
            SimpleNamespace(content_id="x", variant=" a ", score=0.90),
            SimpleNamespace(content_id="x", variant="B", score=0.80),
        ],
        content_id="x",
    )
    assert score == 0.85
    assert state == "mastered"
    assert variants == 2


def test_adaptive_mastery_ignores_invalid_scores_and_non_string_content_ids():
    score, state, variants = summarize_adaptive_mastery(
        [
            SimpleNamespace(content_id=None, variant="a", score=1.0),
            SimpleNamespace(content_id="x", variant="a", score=float("nan")),
            SimpleNamespace(content_id="x", variant="b", score="not-a-score"),
            SimpleNamespace(content_id="x", variant="c", score=0.60),
        ],
        content_id="x",
    )
    assert score == 0.60
    assert state == "learning"
    assert variants == 1


def test_skill_mastery_aggregates_shared_exercises_deterministically():
    exercises = [
        SimpleNamespace(id=1, content_id="alpha", skills=["grammar"]),
        SimpleNamespace(id=2, content_id="beta", skills=["vocabulary", "grammar"]),
        SimpleNamespace(id=3, content_id="gamma", skills=[]),
    ]
    attempts = [
        SimpleNamespace(content_id="alpha", variant="a", score=0.90),
        SimpleNamespace(content_id="alpha", variant="b", score=0.90),
        SimpleNamespace(content_id="beta", variant="a", score=0.60),
    ]

    result = summarize_skill_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_skills=lambda item: item.skills,
    )

    assert [item.skill for item in result] == ["grammar", "vocabulary"]
    grammar, vocabulary = result
    assert grammar.total_exercises == 2
    assert grammar.mastered_exercises == 1
    assert grammar.learning_exercises == 1
    assert grammar.mastery_rate == 0.5
    assert grammar.covered_variants == 3
    assert vocabulary.total_exercises == 1
    assert vocabulary.mastered_exercises == 0
    assert vocabulary.learning_exercises == 1
    assert vocabulary.mastery_rate == 0.0


def test_skill_mastery_normalizes_case_and_deduplicates_labels_per_exercise():
    exercises = [
        SimpleNamespace(id=1, content_id="alpha", skills=["Grammar", " grammar ", "GRAMMAR"]),
        SimpleNamespace(id=2, content_id="beta", skills=["GRAMMAR"]),
    ]
    attempts = [
        SimpleNamespace(content_id="alpha", variant="a", score=0.90),
        SimpleNamespace(content_id="alpha", variant="b", score=0.90),
        SimpleNamespace(content_id="beta", variant="a", score=0.60),
    ]

    result = summarize_skill_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_skills=lambda item: item.skills,
    )

    assert len(result) == 1
    assert result[0].skill == "grammar"
    assert result[0].total_exercises == 2
    assert result[0].mastered_exercises == 1
    assert result[0].learning_exercises == 1
    assert result[0].covered_variants == 3


def test_skill_mastery_accepts_single_skill_strings_and_ignores_blank_labels():
    exercises = [
        SimpleNamespace(id=1, content_id="alpha", skills="pronunciation"),
        SimpleNamespace(id=2, content_id="beta", skills=["", " "]),
    ]
    attempts = [
        SimpleNamespace(content_id="alpha", variant="a", score=0.80),
    ]

    result = summarize_skill_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_skills=lambda item: item.skills,
    )

    assert len(result) == 1
    assert result[0].skill == "pronunciation"
    assert result[0].attempted_exercises == 1


def test_skill_mastery_ignores_non_string_and_blank_skill_labels():
    exercises = [
        SimpleNamespace(id=1, content_id="alpha", skills=[None, "", " grammar ", 42]),
        SimpleNamespace(id=2, content_id="beta", skills=["grammar"]),
    ]
    attempts = [
        SimpleNamespace(content_id="alpha", variant="a", score=0.90),
        SimpleNamespace(content_id="alpha", variant="b", score=0.90),
        SimpleNamespace(content_id="beta", variant="a", score=0.60),
    ]

    result = summarize_skill_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_skills=lambda item: item.skills,
    )

    assert [item.skill for item in result] == ["grammar"]
    assert result[0].total_exercises == 2
    assert result[0].covered_variants == 3


def test_skill_mastery_exposes_aggregate_state_from_exercise_states():
    exercises = [
        SimpleNamespace(id=1, content_id="alpha", skills=["grammar"]),
        SimpleNamespace(id=2, content_id="beta", skills=["grammar"]),
        SimpleNamespace(id=3, content_id="gamma", skills=["grammar"]),
    ]
    attempts = [
        SimpleNamespace(content_id="alpha", variant="a", score=0.90),
        SimpleNamespace(content_id="alpha", variant="b", score=0.90),
        SimpleNamespace(content_id="beta", variant="a", score=0.20),
    ]

    result = summarize_skill_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_skills=lambda item: item.skills,
    )

    assert result[0].mastery_state == "struggling"


def test_skill_mastery_reports_unseen_and_learning_states():
    unseen = summarize_skill_mastery(
        [SimpleNamespace(id=1, content_id="alpha", skills=["grammar"])],
        [],
        get_content_id=lambda item: item.content_id,
        get_skills=lambda item: item.skills,
    )
    assert unseen[0].mastery_state == "unseen"

    learning = summarize_skill_mastery(
        [
            SimpleNamespace(id=1, content_id="alpha", skills=["grammar"]),
            SimpleNamespace(id=2, content_id="beta", skills=["grammar"]),
        ],
        [
            SimpleNamespace(content_id="alpha", variant="a", score=0.70),
            SimpleNamespace(content_id="beta", variant="a", score=0.90),
        ],
        get_content_id=lambda item: item.content_id,
        get_skills=lambda item: item.skills,
    )
    assert learning[0].mastery_state == "learning"


def test_skill_mastery_is_mastered_only_when_every_exercise_is_mastered():
    exercises = [
        SimpleNamespace(id=1, content_id="alpha", skills=["grammar"]),
        SimpleNamespace(id=2, content_id="beta", skills=["grammar"]),
    ]
    attempts = [
        SimpleNamespace(content_id="alpha", variant="a", score=0.90),
        SimpleNamespace(content_id="alpha", variant="b", score=0.90),
        SimpleNamespace(content_id="beta", variant="a", score=0.90),
        SimpleNamespace(content_id="beta", variant="b", score=0.90),
    ]

    result = summarize_skill_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_skills=lambda item: item.skills,
    )

    assert result[0].mastery_state == "mastered"


def test_skill_mastery_exposes_attempt_rate_and_variant_coverage():
    exercises = [
        SimpleNamespace(id=1, content_id="alpha", skills=["grammar"]),
        SimpleNamespace(id=2, content_id="beta", skills=["grammar"]),
    ]
    attempts = [
        SimpleNamespace(content_id="alpha", variant="a", score=0.90),
        SimpleNamespace(content_id="alpha", variant="b", score=0.90),
        SimpleNamespace(content_id="beta", variant="a", score=0.60),
    ]

    result = summarize_skill_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_skills=lambda item: item.skills,
    )

    assert len(result) == 1
    assert result[0].attempt_rate == 1.0
    assert result[0].covered_variants == 3


def test_lesson_mastery_response_embeds_skill_snapshots():
    response = LessonMasteryResponse(
        mastery_state="learning",
        total_exercises=2,
        attempted_exercises=2,
        mastered_exercises=1,
        learning_exercises=1,
        struggling_exercises=0,
        unseen_exercises=0,
        average_mastery_score=0.75,
        attempt_rate=1.0,
        mastery_rate=0.5,
        covered_variants=3,
        skills=[
            {
                "skill": "grammar",
                "mastery_state": "learning",
                "total_exercises": 2,
                "attempted_exercises": 2,
                "mastered_exercises": 1,
                "learning_exercises": 1,
                "struggling_exercises": 0,
                "unseen_exercises": 0,
                "average_mastery_score": 0.75,
                "mastery_rate": 0.5,
                "attempt_rate": 1.0,
                "covered_variants": 3,
            }
        ],
    )

    assert len(response.skills) == 1
    assert response.skills[0].skill == "grammar"
    assert response.skills[0].mastery_rate == 0.5


def test_next_skill_mastery_prioritizes_struggling_then_unseen_then_learning():
    aggregates = [
        SimpleNamespace(skill="learning", mastery_state="learning", mastery_rate=0.10, average_mastery_score=0.60),
        SimpleNamespace(skill="unseen", mastery_state="unseen", mastery_rate=0.0, average_mastery_score=0.0),
        SimpleNamespace(skill="struggling", mastery_state="struggling", mastery_rate=0.25, average_mastery_score=0.20),
        SimpleNamespace(skill="mastered", mastery_state="mastered", mastery_rate=1.0, average_mastery_score=0.90),
    ]

    result = select_next_skill_mastery(aggregates)

    assert result is aggregates[2]


def test_next_skill_mastery_breaks_equal_priority_by_rate_then_score_then_name():
    aggregates = [
        SimpleNamespace(skill="zeta", mastery_state="learning", mastery_rate=0.40, average_mastery_score=0.50),
        SimpleNamespace(skill="alpha", mastery_state="learning", mastery_rate=0.40, average_mastery_score=0.50),
        SimpleNamespace(skill="beta", mastery_state="learning", mastery_rate=0.40, average_mastery_score=0.60),
        SimpleNamespace(skill="gamma", mastery_state="learning", mastery_rate=0.30, average_mastery_score=0.90),
    ]

    result = select_next_skill_mastery(aggregates)

    assert result is aggregates[3]


def test_next_skill_mastery_returns_none_when_all_skills_are_mastered():
    aggregates = [
        SimpleNamespace(skill="grammar", mastery_state="mastered", mastery_rate=1.0, average_mastery_score=0.90),
        SimpleNamespace(skill="vocabulary", mastery_state="mastered", mastery_rate=1.0, average_mastery_score=0.90),
    ]

    assert select_next_skill_mastery(aggregates) is None
