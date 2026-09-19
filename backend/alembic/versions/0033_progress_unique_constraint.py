"""Add unique constraint on progress (user_id, study_plan_id, date)

Revision ID: 0033_progress_unique_constraint
Revises: 0032_attempts_study_plan_id
Create Date: 2026-06-05
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0033_progress_unique_constraint"
down_revision: str | None = "0032_attempts_study_plan_id"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Keep the oldest row in each duplicate group, merge additive counters,
    # and retain the latest skills payload. This avoids PostgreSQL-only JSONB
    # operators while preserving the important progress totals.
    op.execute("""
        UPDATE progress
        SET xp_earned = (
                SELECT SUM(p2.xp_earned)
                FROM progress AS p2
                WHERE p2.user_id = progress.user_id
                  AND p2.study_plan_id = progress.study_plan_id
                  AND p2.date = progress.date
            ),
            lessons_completed = (
                SELECT SUM(p2.lessons_completed)
                FROM progress AS p2
                WHERE p2.user_id = progress.user_id
                  AND p2.study_plan_id = progress.study_plan_id
                  AND p2.date = progress.date
            ),
            exercises_correct = (
                SELECT SUM(p2.exercises_correct)
                FROM progress AS p2
                WHERE p2.user_id = progress.user_id
                  AND p2.study_plan_id = progress.study_plan_id
                  AND p2.date = progress.date
            ),
            exercises_total = (
                SELECT SUM(p2.exercises_total)
                FROM progress AS p2
                WHERE p2.user_id = progress.user_id
                  AND p2.study_plan_id = progress.study_plan_id
                  AND p2.date = progress.date
            ),
            streak_day = (
                SELECT MAX(p2.streak_day)
                FROM progress AS p2
                WHERE p2.user_id = progress.user_id
                  AND p2.study_plan_id = progress.study_plan_id
                  AND p2.date = progress.date
            ),
            skills = (
                SELECT p2.skills
                FROM progress AS p2
                WHERE p2.user_id = progress.user_id
                  AND p2.study_plan_id = progress.study_plan_id
                  AND p2.date = progress.date
                ORDER BY p2.id DESC
                LIMIT 1
            )
        WHERE id IN (
            SELECT MIN(p3.id)
            FROM progress AS p3
            GROUP BY p3.user_id, p3.study_plan_id, p3.date
            HAVING COUNT(*) > 1
        )
    """)

    op.execute("""
        DELETE FROM progress
        WHERE EXISTS (
            SELECT 1
            FROM progress AS keeper
            WHERE keeper.user_id = progress.user_id
              AND keeper.study_plan_id = progress.study_plan_id
              AND keeper.date = progress.date
              AND keeper.id < progress.id
        )
    """)

    with op.batch_alter_table("progress", recreate="auto") as batch_op:
        batch_op.create_unique_constraint(
            "uq_progress_user_plan_date",
            ["user_id", "study_plan_id", "date"],
        )


def downgrade() -> None:
    with op.batch_alter_table("progress", recreate="auto") as batch_op:
        batch_op.drop_constraint("uq_progress_user_plan_date", type_="unique")
