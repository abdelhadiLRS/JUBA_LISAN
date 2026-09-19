"""Fix study_plans.target_language from user_languages where mismatched

Revision ID: 0038_fix_plan_target_lang
Revises: 0037_backfill_chat_history_spid
Create Date: 2026-06-06
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0038_fix_plan_target_lang"
down_revision: str | None = "0037_backfill_chat_history_spid"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        UPDATE study_plans
        SET target_language = (
            SELECT ul.target_language
            FROM user_languages AS ul
            WHERE ul.id = study_plans.user_language_id
        )
        WHERE user_language_id IS NOT NULL
          AND target_language != (
              SELECT ul.target_language
              FROM user_languages AS ul
              WHERE ul.id = study_plans.user_language_id
          )
    """)


def downgrade() -> None:
    pass
