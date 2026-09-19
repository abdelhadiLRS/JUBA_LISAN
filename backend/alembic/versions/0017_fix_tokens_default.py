"""Fix monthly_tokens_limit server default to 1000000 (was 0)

Revision ID: 0017_fix_tokens_default
Revises: 0016_stripe_subscription
Create Date: 2026-05-11
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0017_fix_tokens_default"
down_revision: str | None = "0016_stripe_subscription"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("users", recreate="auto") as batch_op:
        batch_op.alter_column(
            "monthly_tokens_limit",
            existing_type=sa.Integer(),
            server_default="1000000",
            existing_nullable=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("users", recreate="auto") as batch_op:
        batch_op.alter_column(
            "monthly_tokens_limit",
            existing_type=sa.Integer(),
            server_default="0",
            existing_nullable=False,
        )
