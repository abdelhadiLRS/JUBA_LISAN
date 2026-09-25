"""Store missed game-question snapshots for adaptive review.

Revision ID: 0058_game_progress_event_mistakes
Revises: 0057_game_session_daily_challenge
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0058_game_progress_event_mistakes"
down_revision: str | None = "0057_game_session_daily_challenge"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "game_progress_events",
        sa.Column("mistakes", sa.JSON(), nullable=False, server_default="[]"),
    )


def downgrade() -> None:
    op.drop_column("game_progress_events", "mistakes")
