"""Persist game statistics and achievements per study plan.

Revision ID: 0053_game_progress
Revises: 0052_desktop_refresh_tokens
"""

from alembic import op
import sqlalchemy as sa


revision = "0053_game_progress"
down_revision = "0052_desktop_refresh_tokens"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "game_progress",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("study_plan_id", sa.Integer(), nullable=False),
        sa.Column("games_played", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("questions_answered", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("correct_answers", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("best_round_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("daily_challenges_completed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_daily_challenge_date", sa.String(length=10), nullable=False, server_default=""),
        sa.Column("current_correct_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("best_correct_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("achievements", sa.JSON(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["study_plan_id"], ["study_plans.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "study_plan_id", name="uq_game_progress_user_plan"),
    )
    op.create_index("ix_game_progress_user_id", "game_progress", ["user_id"], unique=False)
    op.create_index("ix_game_progress_study_plan_id", "game_progress", ["study_plan_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_game_progress_study_plan_id", table_name="game_progress")
    op.drop_index("ix_game_progress_user_id", table_name="game_progress")
    op.drop_table("game_progress")
