"""Track claimed daily and weekly goal rewards.

Revision ID: 0060_learning_goal_rewards
Revises: 0059_learning_goals
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0060_learning_goal_rewards"
down_revision: str | None = "0059_learning_goals"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("learning_goals", sa.Column("daily_reward_date", sa.Date(), nullable=True))
    op.add_column("learning_goals", sa.Column("weekly_reward_start", sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column("learning_goals", "weekly_reward_start")
    op.drop_column("learning_goals", "daily_reward_date")
