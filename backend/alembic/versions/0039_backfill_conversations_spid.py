"""Backfill study_plan_id for existing conversations rows

Revision ID: 0039_backfill_conversations_spid
Revises: 0038_fix_plan_target_lang
Create Date: 2026-06-15
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0039_backfill_conversations_spid"
down_revision: str | None = "0038_fix_plan_target_lang"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        UPDATE conversations
        SET study_plan_id = (
            SELECT sp.id
            FROM study_plans AS sp
            WHERE sp.user_id = conversations.user_id
              AND sp.is_active = true
            ORDER BY sp.created_at DESC, sp.id DESC
            LIMIT 1
        )
        WHERE study_plan_id IS NULL
    """)


def downgrade() -> None:
    pass
