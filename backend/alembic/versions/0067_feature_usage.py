"""Durable account-wide feature usage and in-flight reservations."""
from alembic import op
import sqlalchemy as sa
revision = "0067_feature_usage"
down_revision = "0066_subscription_tiers"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("feature_usage",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("feature", sa.String(24), nullable=False),
        sa.Column("period_start", sa.DateTime(), nullable=False),
        sa.Column("used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reserved", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("user_id", "feature", "period_start", name="uq_feature_usage_period"),
        sa.CheckConstraint("used >= 0 AND reserved >= 0", name="ck_feature_usage_nonnegative"))
    op.create_table("feature_reservations",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("usage_id", sa.Integer(), sa.ForeignKey("feature_usage.id", ondelete="CASCADE"), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("state", sa.String(12), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("amount > 0", name="ck_feature_reservation_amount"))
    op.create_index("ix_feature_reservations_usage_id", "feature_reservations", ["usage_id"])


def downgrade() -> None:
    op.drop_table("feature_reservations")
    op.drop_table("feature_usage")
