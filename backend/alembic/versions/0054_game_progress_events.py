"""Add idempotent server-recorded game completion events.

Revision ID: 0054_game_progress_events
Revises: 0053_game_progress
"""

from alembic import op
import sqlalchemy as sa


revision = "0054_game_progress_events"
down_revision = "0053_game_progress"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "game_progress_events",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("event_id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("study_plan_id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.String(length=32), nullable=False),
        sa.Column("questions_answered", sa.Integer(), nullable=False),
        sa.Column("correct_answers", sa.Integer(), nullable=False),
        sa.Column("round_score", sa.Integer(), nullable=False),
        sa.Column("daily_challenge", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("daily_challenge_date", sa.String(length=10), nullable=False, server_default=""),
        sa.Column("achievements", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["study_plan_id"], ["study_plans.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "study_plan_id",
            "event_id",
            name="uq_game_progress_event_user_plan_event",
        ),
    )
    op.create_index(
        "ix_game_progress_events_user_id",
        "game_progress_events",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_game_progress_events_study_plan_id",
        "game_progress_events",
        ["study_plan_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_game_progress_events_study_plan_id", table_name="game_progress_events")
    op.drop_index("ix_game_progress_events_user_id", table_name="game_progress_events")
    op.drop_table("game_progress_events")
