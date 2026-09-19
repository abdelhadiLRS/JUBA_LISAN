"""Add unique constraint to lessons (study_plan_id, week_number, day_number, title)

Revision ID: 0024_lessons_unique
Revises: 0023_exercise_explanation
Create Date: 2026-05-24
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0024_lessons_unique"
down_revision: str | None = "0023_exercise_explanation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Remove duplicate lessons before adding the unique constraint.
    # Keep the completed lesson when a duplicate group contains one;
    # otherwise keep the oldest lesson. The correlated subquery is supported
    # by both PostgreSQL and SQLite, unlike PostgreSQL-only DISTINCT ON.
    op.execute("""
        DELETE FROM lessons AS lesson
        WHERE lesson.id <> (
            SELECT keeper.id
            FROM lessons AS keeper
            WHERE keeper.study_plan_id = lesson.study_plan_id
              AND keeper.week_number = lesson.week_number
              AND keeper.day_number = lesson.day_number
              AND keeper.title = lesson.title
            ORDER BY keeper.is_completed DESC, keeper.id ASC
            LIMIT 1
        )
    """)

    with op.batch_alter_table("lessons", recreate="auto") as batch_op:
        batch_op.create_unique_constraint(
            "uq_lessons_plan_week_day_title",
            ["study_plan_id", "week_number", "day_number", "title"],
        )


def downgrade() -> None:
    with op.batch_alter_table("lessons", recreate="auto") as batch_op:
        batch_op.drop_constraint("uq_lessons_plan_week_day_title", type_="unique")
