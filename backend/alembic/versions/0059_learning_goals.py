"""Persist daily and weekly XP goals per active study plan.

Revision ID: 0059_learning_goals
Revises: 0058_exercise_attempts
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0059_learning_goals"
down_revision: str | None = "0058_exercise_attempts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "learning_goals",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("study_plan_id", sa.Integer(), nullable=False),
        sa.Column("daily_xp_target", sa.Integer(), nullable=False, server_default="50"),
        sa.Column("weekly_xp_target", sa.Integer(), nullable=False, server_default="250"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["study_plan_id"], ["study_plans.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "study_plan_id", name="uq_learning_goal_user_plan"),
    )
    op.create_index("ix_learning_goals_user_id", "learning_goals", ["user_id"])
    op.create_index("ix_learning_goals_study_plan_id", "learning_goals", ["study_plan_id"])


def downgrade() -> None:
    op.drop_index("ix_learning_goals_study_plan_id", table_name="learning_goals")
    op.drop_index("ix_learning_goals_user_id", table_name="learning_goals")
    op.drop_table("learning_goals")
