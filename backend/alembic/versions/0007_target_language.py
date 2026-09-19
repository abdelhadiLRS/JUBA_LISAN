"""Rename english_variant to target_language (BCP-47); add study_plans.target_language

Revision ID: 0007_target_language
Revises: 0006_conversation_timeouts
Create Date: 2026-05-04
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0007_target_language"
down_revision: str | None = "0006_conversation_timeouts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("target_language", sa.String(10), nullable=True))
    op.execute("""
        UPDATE users
        SET target_language = CASE
            WHEN english_variant = 'british' THEN 'en-GB'
            ELSE 'en-US'
        END
        """)
    with op.batch_alter_table("users", recreate="auto") as batch_op:
        batch_op.alter_column("target_language", nullable=False, server_default="en-US")
        batch_op.drop_column("english_variant")

    op.add_column("study_plans", sa.Column("target_language", sa.String(10), nullable=True))
    op.execute("UPDATE study_plans SET target_language = 'en-US'")
    with op.batch_alter_table("study_plans", recreate="auto") as batch_op:
        batch_op.alter_column("target_language", nullable=False, server_default="en-US")


def downgrade() -> None:
    with op.batch_alter_table("study_plans", recreate="auto") as batch_op:
        batch_op.drop_column("target_language")

    op.add_column("users", sa.Column("english_variant", sa.String(10), nullable=True))
    op.execute("""
        UPDATE users
        SET english_variant = CASE
            WHEN target_language = 'en-GB' THEN 'british'
            ELSE 'american'
        END
        """)
    with op.batch_alter_table("users", recreate="auto") as batch_op:
        batch_op.alter_column("english_variant", nullable=False, server_default="american")
        batch_op.drop_column("target_language")