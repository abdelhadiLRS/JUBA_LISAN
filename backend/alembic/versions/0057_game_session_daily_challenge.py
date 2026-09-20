"""Persist the server-selected daily challenge slot on game sessions.

Revision ID: 0057_game_session_daily_challenge
Revises: 0056_ai_sessions_and_schema_alignment
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0057_game_session_daily_challenge"
down_revision: str | None = "0056_ai_sessions_and_schema_alignment"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Keep the migration SQLite-compatible. The temporary server default is
    # intentionally retained because SQLite cannot drop a column default with
    # a plain ALTER COLUMN statement.
    op.add_column(
        "game_sessions",
        sa.Column(
            "daily_challenge_date",
            sa.String(length=10),
            nullable=False,
            server_default="",
        ),
    )


def downgrade() -> None:
    op.drop_column("game_sessions", "daily_challenge_date")
