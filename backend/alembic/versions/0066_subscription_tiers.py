"""Persist product tier; preserve all existing paid subscribers as Plus."""
from alembic import op
import sqlalchemy as sa

revision = "0066_subscription_tiers"
down_revision = "0065_leagues"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("subscription_tier", sa.String(10), nullable=False, server_default="free"))
    op.execute("UPDATE users SET subscription_tier = 'plus' WHERE stripe_subscription_id IS NOT NULL OR subscription_status IN ('active', 'trialing', 'past_due', 'unpaid', 'paused')")


def downgrade() -> None:
    with op.batch_alter_table("users") as batch:
        batch.drop_column("subscription_tier")
