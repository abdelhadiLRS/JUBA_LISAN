"""Add server-issued game sessions.

Revision ID: 0054_game_sessions
Revises: 0053_game_progress
"""

from alembic import op
import sqlalchemy as sa

revision = "0054_game_sessions"
down_revision = "0053_game_progress"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "game_sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("study_plan_id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.String(length=32), nullable=False),
        sa.Column("language", sa.String(length=10), nullable=False),
        sa.Column("difficulty", sa.Integer(), nullable=False),
        sa.Column("questions", sa.JSON(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.ForeignKeyConstraint(["study_plan_id"], ["study_plans.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_game_sessions_user_id", "game_sessions", ["user_id"], unique=False)
    op.create_index("ix_game_sessions_study_plan_id", "game_sessions", ["study_plan_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_game_sessions_study_plan_id", table_name="game_sessions")
    op.drop_index("ix_game_sessions_user_id", table_name="game_sessions")
    op.drop_table("game_sessions")
