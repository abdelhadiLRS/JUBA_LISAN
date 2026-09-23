from app.data.ar.lessons import get_arabic_a1_content_seed


def test_arabic_a1_seed_is_available():
    seed = get_arabic_a1_content_seed("a1-u1-w1-d1")
    assert seed is not None
    assert "مرحبًا، أنا أحمد." in seed.target_phrases
    assert "أنا طالب." in seed.model_sentences


def test_unknown_lesson_has_no_seed():
    assert get_arabic_a1_content_seed("a1-u8-w2-d5") is None
