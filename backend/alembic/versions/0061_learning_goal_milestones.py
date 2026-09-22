"""Persist daily and weekly learning goal milestone history.

Revision ID: 0061_learning_goal_milestones
Revises: 0060_learning_goal_rewards
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0061_learning_goal_milestones"
down_revision: str | None = "0060_learning_goal_rewards"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "learning_goal_milestones",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("study_plan_id", sa.Integer(), nullable=False),
        sa.Column("goal_type", sa.String(length=16), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("target_xp", sa.Integer(), nullable=False),
        sa.Column("achieved_xp", sa.Integer(), nullable=False),
        sa.Column("reward_xp", sa.Integer(), nullable=False),
        sa.Column("achieved_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["study_plan_id"], ["study_plans.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "study_plan_id",
            "goal_type",
            "period_start",
            name="uq_learning_goal_milestone_period",
        ),
    )
    op.create_index("ix_learning_goal_milestones_user_id", "learning_goal_milestones", ["user_id"])
    op.create_index("ix_learning_goal_milestones_study_plan_id", "learning_goal_milestones", ["study_plan_id"])


def downgrade() -> None:
    op.drop_index("ix_learning_goal_milestones_study_plan_id", table_name="learning_goal_milestones")
    op.drop_index("ix_learning_goal_milestones_user_id", table_name="learning_goal_milestones")
    op.drop_table("learning_goal_milestones")
