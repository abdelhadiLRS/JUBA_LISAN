"""Track reward XP separately from learning activity XP.

Revision ID: 0062_progress_reward_xp
Revises: 0061_learning_goal_milestones, 0051_friend_connection_pair_key
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0062_progress_reward_xp"
down_revision: tuple[str, str] = ("0061_learning_goal_milestones", "0051_friend_connection_pair_key")
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "progress",
        sa.Column("reward_xp", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("progress", "reward_xp")
