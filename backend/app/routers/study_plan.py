@limiter.limit("60/minute")
async def get_pending_lessons(
    request: Request,
    plan: StudyPlan = Depends(get_active_study_plan),
    db: AsyncSession = Depends(get_db),
):
    incomplete_result = await db.execute(
        select(Lesson).where(
            Lesson.study_plan_id == plan.id,
            Lesson.is_completed.is_(False),
        )
    )
    pending = [
        lsn
        for lsn in incomplete_result.scalars().all()
        if (lsn.week_number - 1) * plan.days_per_week + (lsn.day_number - 1) < plan.progress_day
    ]
    return pending


@router.get("/lessons", response_model=list[PlanLessonResponse])
@limiter.limit("60/minute")
async def get_plan_lessons(
    request: Request,
    plan: StudyPlan = Depends(get_active_study_plan),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Lesson)
        .where(Lesson.study_plan_id == plan.id)
        .order_by(Lesson.week_number, Lesson.day_number, Lesson.id)
    )
    return result.scalars().all()


def _lesson_slot_index(lesson: Lesson, days_per_week: int) -> int:
    return (lesson.week_number - 1) * days_per_week + (lesson.day_number - 1)


async def _learning_path_state(
    db: AsyncSession,
    user_id: int,
    plan: StudyPlan,
) -> tuple[list[LearningJourneySectionResponse], int | None, str | None]:
    from app.data.curriculum import get_curriculum_units

    units = get_curriculum_units(plan.cefr_level, plan.target_language)
    lessons_result = await db.execute(
        select(Lesson)
        .where(Lesson.study_plan_id == plan.id)
        .order_by(Lesson.week_number, Lesson.day_number, Lesson.id)
    )
    persisted = lessons_result.scalars().all()
    lessons_by_unit: dict[str, list[Lesson]] = defaultdict(list)
    for lesson in persisted:
        if lesson.unit_id:
            lessons_by_unit[lesson.unit_id].append(lesson)

    competency_rows = await get_unit_competencies(db, user_id, study_plan_id=plan.id)
    competency_map = {row["unit_id"]: row for row in competency_rows}

    # Keep journey metadata aligned with the persisted study-plan blueprint.
    # This lets the journey render objectives/duration even before a lesson is opened.
    plan_day_meta: dict[tuple[int, int], dict] = {}
    for week in _get_weekly_plan_items(plan.generated_plan):
        week_number = _get_plan_value(week, "week")
        if not isinstance(week_number, int):
            continue
        for day in _get_week_days(week):
            day_number = _get_plan_value(day, "day")
            if isinstance(day_number, int):
                plan_day_meta[(week_number, day_number)] = {
                    "title": _get_plan_value(day, "title", ""),
                    "objectives": _get_plan_value(day, "objectives", []),
                    "estimated_minutes": _get_plan_value(day, "estimated_minutes", 25),
                }

    # A competency score is live evidence, not by itself proof that the whole
    # curriculum unit is finished. Count the lesson slots assigned to each unit
    # in the persisted study-plan blueprint so one excellent exercise cannot
    # prematurely complete/unlock an entire unit.
    expected_slots_by_unit: dict[str, int] = defaultdict(int)
    for week in _get_weekly_plan_items(plan.generated_plan):
        for day in _get_week_days(week):
            unit_id = _get_plan_value(day, "unit_id")
            if isinstance(unit_id, str) and unit_id:
                expected_slots_by_unit[unit_id] += 1

    sections: list[LearningJourneySectionResponse] = []
    previous_unit_id: str | None = None
    next_lesson_id: int | None = None
    next_unit_id: str | None = None

    section_units: list[LearningJourneyUnitResponse] = []
    for unit in units:
        unit_lessons = lessons_by_unit.get(unit.id, [])
        unit_score = float(competency_map.get(unit.id, {}).get("score", 0.0))
        mastered_count = int(competency_map.get(unit.id, {}).get("mastered_count", 0))
        competency_count = int(competency_map.get(unit.id, {}).get("total_count", len(unit.competency_checklist)))

        completed_count = sum(1 for lesson in unit_lessons if lesson.is_completed)
        expected_slots = expected_slots_by_unit.get(unit.id, 0)
        unit_complete = expected_slots > 0 and completed_count >= expected_slots
        prereq = unit.prerequisite_unit
        prereq_score = float(competency_map.get(prereq, {}).get("score", 0.0)) if prereq else 1.0
        prereq_complete = not prereq or prereq_score >= 0.80

        if unit_complete:
            state = "completed"
        elif prereq_complete and (prereq is None or previous_unit_id == prereq):
            state = "active"
        elif prereq_complete and not unit_lessons:
            state = "available"
        else:
            state = "locked"

        lesson_responses: list[LearningJourneyLessonResponse] = []
        ordered_slots = sorted(unit_lessons, key=lambda item: (_lesson_slot_index(item, plan.days_per_week), item.id))
        prior_complete = True
        for lesson in ordered_slots:
            slot_index = _lesson_slot_index(lesson, plan.days_per_week)
            available = state in {"active", "available"} and prior_complete
            lesson_state = "completed" if lesson.is_completed else ("available" if available else "locked")
            meta = plan_day_meta.get((lesson.week_number, lesson.day_number), {})
            objectives = meta.get("objectives", [])
            estimated_minutes = meta.get("estimated_minutes", 25)
            if not isinstance(objectives, list):
                objectives = []
            objectives = [item for item in objectives if isinstance(item, str)]
            if isinstance(estimated_minutes, bool) or not isinstance(estimated_minutes, (int, float)) or estimated_minutes <= 0:
                estimated_minutes = 25
            lesson_responses.append(
                LearningJourneyLessonResponse(
                    id=lesson.id,
                    title=lesson.title,
                    lesson_type=lesson.lesson_type,
                    week_number=lesson.week_number,
                    day_number=lesson.day_number,
                    unit_id=unit.id,
                    is_completed=lesson.is_completed,
                    available=available,
                    state=lesson_state,
                    objectives=objectives,
                    estimated_minutes=int(estimated_minutes),
                )
            )
            if not lesson.is_completed:
                prior_complete = False
                if available and next_lesson_id is None:
                    next_lesson_id = lesson.id
                    next_unit_id = unit.id

        section_units.append(
            LearningJourneyUnitResponse(
                id=unit.id,
                title=unit.title,
                level=unit.level,
                unit_number=unit.unit_number,
                prerequisite_unit=prereq,
                state=state,
                progress=round(unit_score, 3),
                mastered_count=mastered_count,
                competency_count=competency_count,
                lessons=lesson_responses,
            )
        )
        if unit_complete:
            previous_unit_id = unit.id

    sections.append(
        LearningJourneySectionResponse(