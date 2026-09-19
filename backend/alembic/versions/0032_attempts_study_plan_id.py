"""Add study_plan_id to listening_attempts and reading_attempts

Revision ID: 0032_attempts_study_plan_id
Revises: 0031_not_null_study_plan_id
Create Date: 2026-06-05
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0032_attempts_study_plan_id"
down_revision: str | None = "0031_not_null_study_plan_id"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _add_fk(table: str, constraint_name: str) -> None:
    with op.batch_alter_table(table, recreate="auto") as batch_op:
        batch_op.create_foreign_key(
            constraint_name,
            "study_plans",
            ["study_plan_id"],
            ["id"],
            ondelete="CASCADE",
        )


def _drop_fk(table: str, constraint_name: str) -> None:
    with op.batch_alter_table(table, recreate="auto") as batch_op:
        batch_op.drop_constraint(constraint_name, type_="foreignkey")


def upgrade() -> None:
    for table in ("listening_attempts", "reading_attempts"):
        op.add_column(table, sa.Column("study_plan_id", sa.Integer(), nullable=True))
        _add_fk(table, f"fk_{table}_study_plan")
        op.create_index(f"ix_{table}_study_plan_id", table, ["study_plan_id"])

    op.execute("""
        UPDATE listening_attempts
        SET study_plan_id = (
            SELECT sp.id
            FROM study_plans AS sp
            JOIN listening_exercises AS le ON le.id = listening_attempts.exercise_id
            WHERE sp.user_id = listening_attempts.user_id
              AND sp.target_language = le.target_language
              AND sp.is_active = true
            ORDER BY sp.created_at DESC, sp.id DESC
            LIMIT 1
        )
        WHERE study_plan_id IS NULL
        """)
    op.execute("""
        UPDATE reading_attempts
        SET study_plan_id = (
            SELECT sp.id
            FROM study_plans AS sp
            JOIN reading_exercises AS re ON re.id = reading_attempts.exercise_id
            WHERE sp.user_id = reading_attempts.user_id
              AND sp.target_language = re.target_language
              AND sp.is_active = true
            ORDER BY sp.created_at DESC, sp.id DESC
            LIMIT 1
        )
        WHERE study_plan_id IS NULL
        """)

    for source_table, exercise_table, language_column in (
        ("listening_attempts", "listening_exercises", "target_language"),
        ("reading_attempts", "reading_exercises", "target_language"),
    ):
        op.execute(f"""
            INSERT INTO study_plans (
                user_id, cefr_level, target_language, goals,
                duration_weeks, days_per_week, current_unit, progress_day,
                generated_plan, is_active, completion_test_taken, created_at
            )
            SELECT orphan.user_id, 'A1', orphan.target_language, '[]',
                   12, 4, '', 0, '{{}}', true, false, CURRENT_TIMESTAMP
            FROM (
                SELECT a.user_id, e.{language_column} AS target_language
                FROM {source_table} AS a
                JOIN {exercise_table} AS e ON e.id = a.exercise_id
                WHERE a.study_plan_id IS NULL
                GROUP BY a.user_id, e.{language_column}
            ) AS orphan
            WHERE NOT EXISTS (
                SELECT 1
                FROM study_plans AS sp
                WHERE sp.user_id = orphan.user_id
                  AND sp.target_language = orphan.target_language
                  AND sp.is_active = true
            )
            """)

    op.execute("""
        UPDATE listening_attempts
        SET study_plan_id = (
            SELECT sp.id
            FROM study_plans AS sp
            JOIN listening_exercises AS le ON le.id = listening_attempts.exercise_id
            WHERE sp.user_id = listening_attempts.user_id
              AND sp.target_language = le.target_language
              AND sp.is_active = true
            ORDER BY sp.created_at DESC, sp.id DESC
            LIMIT 1
        )
        WHERE study_plan_id IS NULL
        """)
    op.execute("""
        UPDATE reading_attempts
        SET study_plan_id = (
            SELECT sp.id
            FROM study_plans AS sp
            JOIN reading_exercises AS re ON re.id = reading_attempts.exercise_id
            WHERE sp.user_id = reading_attempts.user_id
              AND sp.target_language = re.target_language
              AND sp.is_active = true
            ORDER BY sp.created_at DESC, sp.id DESC
            LIMIT 1
        )
        WHERE study_plan_id IS NULL
        """)

    for table in ("listening_attempts", "reading_attempts"):
        with op.batch_alter_table(table, recreate="auto") as batch_op:
            batch_op.alter_column("study_plan_id", nullable=False)


def downgrade() -> None:
    for table in ("reading_attempts", "listening_attempts"):
        op.drop_index(f"ix_{table}_study_plan_id", table_name=table)
        _drop_fk(table, f"fk_{table}_study_plan")
        with op.batch_alter_table(table, recreate="auto") as batch_op:
            batch_op.drop_column("study_plan_id")
