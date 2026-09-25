from app.routers.progress import _review_adaptive_difficulty, _review_game_for_item


def test_review_difficulty_drops_for_weak_items():
    assert _review_adaptive_difficulty(3, 0, 0.2) == 2
    assert _review_adaptive_difficulty(2, 0, 0.35) == 1


def test_review_difficulty_rises_for_stable_items():
    assert _review_adaptive_difficulty(1, 2, 0.85) == 2
    assert _review_adaptive_difficulty(2, 2, 0.95) == 3


def test_review_mechanic_tracks_mastery_state():
    assert _review_game_for_item("vocabulary", "weak") == "quick_choice"
    assert _review_game_for_item("vocabulary", "reviewing") == "word_categories"
    assert _review_game_for_item("grammar", "weak") == "grammar_duel"
    assert _review_game_for_item("grammar", "reviewing") == "fill_blank"
