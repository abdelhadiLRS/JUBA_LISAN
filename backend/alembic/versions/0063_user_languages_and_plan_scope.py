"""Finalize the existing multi-language schema for assessment completion.

The multi-language schema was already introduced by migrations 0029 and 0034.
This revision is intentionally data-only and idempotent: it repairs/backfills
language rows without recreating tables or indexes that already exist.

Revision ID: 0063_user_languages_and_plan_scope
Revises: 0062_progress_reward_xp
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0063_user_languages_and_plan_scope"
down_revision: str | None = "0062_progress_reward_xp"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()

    # 0029 already creates user_languages and 0034 already adds
    # study_plans.user_language_id. Do not recreate either object.
    op.execute(
        sa.text(
            """
            INSERT INTO user_languages (user_id, target_language, is_active, created_at)
            SELECT u.id, COALESCE(u.target_language, 'en-US'), true, CURRENT_TIMESTAMP
            FROM users AS u
            WHERE NOT EXISTS (
                SELECT 1
                FROM user_languages AS ul
                WHERE ul.user_id = u.id
                  AND ul.target_language = COALESCE(u.target_language, 'en-US')
            )
            """
        )
    )

    # Existing study plans created before a language row was available are
    # attached to the matching user-language record.
    op.execute(
        sa.text(
            """
            UPDATE study_plans
            SET user_language_id = (
                SELECT ul.id
                FROM user_languages AS ul
                WHERE ul.user_id = study_plans.user_id
                  AND ul.target_language = study_plans.target_language
                ORDER BY ul.id
                LIMIT 1
            )
            WHERE user_language_id IS NULL
            """
        )
    )

    # Keep only the newest active plan per language before the existing
    # partial unique index is relied upon by assessment completion.
    duplicates = bind.execute(
        sa.text(
            """
            SELECT user_language_id
            FROM study_plans
            WHERE is_active = 1
            GROUP BY user_language_id
            HAVING COUNT(*) > 1
            """
        )
    ).scalars().all()

    for language_id in duplicates:
        plan_ids = bind.execute(
            sa.text(
                """
                SELECT id
                FROM study_plans
                WHERE user_language_id = :language_id
                  AND is_active = 1
                ORDER BY created_at DESC, id DESC
                """
            ),
            {"language_id": language_id},
        ).scalars().all()
        for plan_id in plan_ids[1:]:
            bind.execute(
                sa.text("UPDATE study_plans SET is_active = 0 WHERE id = :id"),
                {"id": plan_id},
            )


def downgrade() -> None:
    # Data repair is intentionally non-destructive and needs no downgrade.
    pass
