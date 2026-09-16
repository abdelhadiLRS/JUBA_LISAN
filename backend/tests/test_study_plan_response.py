from datetime import datetime, timezone

from app.schemas.study_plan import StudyPlanResponse


def _response(generated_plan):
    return StudyPlanResponse(
        id=1,
        user_id=1,
        cefr_level="A1",
        goals=["grammar"],
        duration_weeks=1,
        days_per_week=4,
        current_unit="a1-unit-1",
        generated_plan=generated_plan,
        is_active=True,
        completion_test_taken=False,
        completion_test_score=None,
        completion_test_recommendation=None,
        created_at=datetime.now(timezone.utc),
    )


def test_generated_plan_non_dict_becomes_safe_empty_plan():
    response = _response(None)

    assert response.generated_plan == {"title": "", "weekly_plan": []}


def test_generated_plan_filters_malformed_weeks_and_days():
    response = _response(
        {
            "title": "A1 plan",
            "weekly_plan": [
                None,
                {"week": "1", "days": []},
                {
                    "week": 1,
                    "theme": 123,
                    "days": [
                        None,
                        {"day": "1", "title": "bad"},
                        {
                            "day": 1,
                            "title": "Grammar",
                            "lesson_type": None,
                            "objectives": ["valid", 123],
                            "estimated_minutes": "bad",
                            "unit_id": 42,
                        },
                    ],
                },
            ],
        }
    )

    assert len(response.generated_plan["weekly_plan"]) == 1
    week = response.generated_plan["weekly_plan"][0]
    assert week["week"] == 1
    assert week["theme"] == ""
    assert len(week["days"]) == 1
    day = week["days"][0]
    assert day["title"] == "Grammar"
    assert day["lesson_type"] == "review"
    assert day["objectives"] == ["valid"]
    assert day["estimated_minutes"] == 25
    assert day["unit_id"] == ""


def test_generated_plan_preserves_valid_extra_fields():
    response = _response(
        {
            "title": "A1 plan",
            "custom_field": "keep-me",
            "weekly_plan": [
                {
                    "week": 1,
                    "theme": "Basics",
                    "days": [
                        {
                            "day": 1,
                            "title": "Greetings",
                            "lesson_type": "grammar",
                            "objectives": ["introductions"],
                            "estimated_minutes": 30,
                            "unit_id": "a1-1",
                        }
                    ],
                }
            ],
        }
    )

    assert response.generated_plan["custom_field"] == "keep-me"
    assert response.generated_plan["weekly_plan"][0]["days"][0]["estimated_minutes"] == 30
