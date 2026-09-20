"""Persist immutable exercise answer attempts for adaptive retries.

Revision ID: 0058_exercise_attempts
Revises: 0057_game_session_daily_challenge
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0058_exercise_attempts"
down_revision: str | None = "0057_game_session_daily_challenge"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "exercise_attempts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("lesson_id", sa.Integer(), nullable=False),
        sa.Column("study_plan_id", sa.Integer(), nullable=False),
        sa.Column("content_id", sa.String(length=255), nullable=True),
        sa.Column("variant", sa.String(length=50), nullable=True),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("user_answer", sa.Text(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("feedback", sa.Text(), nullable=False),
        sa.Column("answered_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["exercise_id"], ["exercises.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["lesson_id"], ["lessons.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["study_plan_id"], ["study_plans.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "exercise_id",
            "attempt_number",
            name="uq_exercise_attempt_user_exercise_number",
        ),
    )
    op.create_index("ix_exercise_attempts_user_id", "exercise_attempts", ["user_id"])
    op.create_index("ix_exercise_attempts_exercise_id", "exercise_attempts", ["exercise_id"])
    op.create_index("ix_exercise_attempts_lesson_id", "exercise_attempts", ["lesson_id"])
    op.create_index(
        "ix_exercise_attempts_study_plan_id", "exercise_attempts", ["study_plan_id"]
    )
    op.create_index("ix_exercise_attempts_content_id", "exercise_attempts", ["content_id"])


def downgrade() -> None:
    op.drop_index("ix_exercise_attempts_content_id", table_name="exercise_attempts")
    op.drop_index("ix_exercise_attempts_study_plan_id", table_name="exercise_attempts")
    op.drop_index("ix_exercise_attempts_lesson_id", table_name="exercise_attempts")
    op.drop_index("ix_exercise_attempts_exercise_id", table_name="exercise_attempts")
    op.drop_index("ix_exercise_attempts_user_id", table_name="exercise_attempts")
    op.drop_table("exercise_attempts")
