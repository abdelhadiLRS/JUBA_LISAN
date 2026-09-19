"""Add assessment voice trial flag

Revision ID: 0045_assessment_voice_trial
Revises: 0044_stripe_subscription_id
Create Date: 2026-06-28
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0045_assessment_voice_trial"
down_revision: str | None = "0044_stripe_subscription_id"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "assessment_voice_trial_used",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )


def downgrade() -> None:
    with op.batch_alter_table("users", recreate="auto") as batch_op:
        batch_op.drop_column("assessment_voice_trial_used")
