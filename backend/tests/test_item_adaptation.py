from app.routers.progress import _review_adaptive_difficulty, _review_game_for_item, _review_item_strategy, _review_retry_stage


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
