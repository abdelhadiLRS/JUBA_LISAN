from types import SimpleNamespace

from app.routers.progress import (
    _adapt_question_after_session_miss,
    _item_mastery_from_events,
    _review_adaptive_difficulty,
    _review_game_for_item,
    _review_item_strategy,
    _review_retry_stage,
)


def test_review_difficulty_drops_for_weak_items():
    assert _review_adaptive_difficulty(3, 2, 0.2) == 2
    assert _review_adaptive_difficulty(2, 2, 0.35) == 1


def test_review_difficulty_rises_for_stable_items():
    assert _review_adaptive_difficulty(1, 0, 0.85) == 2
    assert _review_adaptive_difficulty(2, 0, 0.95) == 3


def test_review_mechanic_tracks_mastery_state():
    assert _review_game_for_item("vocabulary", "weak") == "quick_choice"
    assert _review_game_for_item("vocabulary", "reviewing") == "word_categories"
    assert _review_game_for_item("grammar", "weak") == "grammar_duel"
    assert _review_game_for_item("grammar", "reviewing") == "fill_blank"


def test_review_mechanic_respects_retrieval_efficiency():
    assert _review_game_for_item("vocabulary", "reviewing", retrieval_efficiency=0.2, review_streak=2) == "word_categories"
    assert _review_game_for_item("vocabulary", "reviewing", retrieval_efficiency=0.9, review_streak=2) == "word_categories"
    assert _review_game_for_item("vocabulary", "mastered", retrieval_efficiency=0.95, review_streak=4, attempts=4) == "translation_sprint"


def test_review_mechanic_keeps_skill_specific_mechanics():
    assert _review_game_for_item("grammar", "weak", retrieval_efficiency=0.1) == "grammar_duel"
    assert _review_game_for_item("grammar", "reviewing", retrieval_efficiency=0.9, review_streak=2) == "fill_blank"
    assert _review_game_for_item("listening", "learning", retrieval_efficiency=0.8, review_streak=1) == "listen_choose"


def test_review_mechanic_variant_is_skill_specific():
    from app.routers.progress import _review_mechanic_variant

    assert _review_mechanic_variant("vocabulary", "direct_recall", 0) == "definition_recall"
    assert _review_mechanic_variant("grammar", "contextual_transfer", 1) == "guided_production"
    assert _review_mechanic_variant("writing", "production", 2) == "free_production"


def test_review_mechanic_variant_follows_retrieval_strategy():
    from app.routers.progress import _review_mechanic_variant

    assert _review_mechanic_variant("vocabulary", "recognition", 0) == "semantic_category"
    assert _review_mechanic_variant("listening", "contextual_transfer", 0) == "audio_transfer"
    assert _review_mechanic_variant("speaking", "production", 0) == "open_response"


def test_review_strategy_progresses_from_recall_to_production():
    assert _review_item_strategy("weak", 0) == "direct_recall"
    assert _review_item_strategy("learning", 1) == "recognition"
    assert _review_item_strategy("reviewing", 2) == "contextual_transfer"
    assert _review_item_strategy("mastered", 3) == "production"


def test_retry_stage_escalates_within_session():
    assert _review_retry_stage(0) == "initial"
    assert _review_retry_stage(1) == "retry"
    assert _review_retry_stage(2) == "focused_retrieval"
    assert _review_retry_stage(3) == "guided_retrieval"


def test_generic_question_adapts_after_repeated_miss():
    question = {"difficulty": 3, "hint": "Use the context.", "prompt": "Choose.", "choices": ["a", "b"]}
    first = _adapt_question_after_session_miss(question, 1)
    repeated = _adapt_question_after_session_miss(question, 2)
    assert first["difficulty"] == 3
    assert first["retry_stage"] == "retry"
    assert repeated["difficulty"] == 2
    assert repeated["retry_stage"] == "focused_retrieval"


def test_item_mastery_tracks_retry_telemetry():
    question = {
        "skill": "vocabulary",
        "target_language": "en-GB",
        "cefr_level": "A1",
    }
    events = [
        SimpleNamespace(
            created_at=__import__("datetime").datetime(2026, 9, 25, 10, 0, 0),
            mistakes=[{
                "review_key": "word:hello",
                "attempt_count": 1,
                "miss_count": 1,
                "retry_stage": "retry",
                "question": question,
            }],
        ),
        SimpleNamespace(
            created_at=__import__("datetime").datetime(2026, 9, 25, 10, 1, 0),
            mistakes=[{
                "review_key": "word:hello",
                "resolved": True,
                "attempt_count": 2,
                "miss_count": 1,
                "retry_stage": "retry",
                "first_attempt_correct": False,
                "question": question,
            }],
        ),
    ]

    mastery = _item_mastery_from_events(
        events,
        "word:hello",
        skill="vocabulary",
        target_language="en-GB",
        cefr_level="A1",
    )

    assert mastery["misses"] == 1
    assert mastery["resolutions"] == 1
    assert mastery["attempts"] == 2
    assert mastery["first_attempt_successes"] == 0
    assert mastery["retry_resolutions"] == 1
    assert mastery["retrieval_efficiency"] == 0.0


def test_item_mastery_rewards_first_attempt_resolution():
    question = {
        "skill": "vocabulary",
        "target_language": "en-GB",
        "cefr_level": "A1",
    }
    event = SimpleNamespace(
        created_at=__import__("datetime").datetime(2026, 9, 25, 11, 0, 0),
        mistakes=[{
            "review_key": "word:world",
            "resolved": True,
            "attempt_count": 1,
            "miss_count": 0,
            "retry_stage": "initial",
            "first_attempt_correct": True,
            "question": question,
        }],
    )

    mastery = _item_mastery_from_events(
        [event],
        "word:world",
        skill="vocabulary",
        target_language="en-GB",
        cefr_level="A1",
    )

    assert mastery["attempts"] == 1
    assert mastery["first_attempt_successes"] == 1
    assert mastery["retry_resolutions"] == 0
    assert mastery["retrieval_efficiency"] == 1.0


def test_review_variant_drops_transfer_when_retrieval_efficiency_is_low():
    from app.routers.progress import _apply_skill_review_variant

    question = {
        "review_key": "word:test",
        "skill": "vocabulary",
        "word": "test",
        "prompt": "What does 'test' mean?",
        "review_strategy": "contextual_transfer",
        "retrieval_efficiency": 0.2,
    }
    replay = _apply_skill_review_variant(question, 0)
    assert replay["retrieval_stage"] == "recognition"


def test_review_variant_keeps_transfer_for_strong_retrieval():
    from app.routers.progress import _apply_skill_review_variant

    question = {
        "review_key": "word:test",
        "skill": "vocabulary",
        "word": "test",
        "prompt": "What does 'test' mean?",
        "review_strategy": "contextual_transfer",
        "retrieval_efficiency": 0.9,
    }
    replay = _apply_skill_review_variant(question, 0)
    assert replay["retrieval_stage"] == "contextual_transfer"
