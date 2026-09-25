"""Merge adaptive-game and user-language migration heads.

Revision ID: 0064_merge_game_mistakes_and_user_languages
Revises: 0058_game_progress_event_mistakes, 0063_user_languages_and_plan_scope
"""

from collections.abc import Sequence

revision: str = "0064_merge_game_mistakes_and_user_languages"
down_revision: tuple[str, str] = (
    "0058_game_progress_event_mistakes",
    "0063_user_languages_and_plan_scope",
)
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Merge-only revision: both parent migrations have already run.
    pass


def downgrade() -> None:
    # Keep both migration branches intact when downgrading this merge point.
    pass
