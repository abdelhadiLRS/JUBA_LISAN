"""One durable pending checkout intent per account."""
from alembic import op
import sqlalchemy as sa
revision = "0068_billing_intents"
down_revision = "0067_feature_usage"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("billing_intents",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("identifier", sa.String(36), nullable=False),
        sa.Column("tier", sa.String(10), nullable=False),
        sa.Column("interval", sa.String(10), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("url", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_table("billing_intents")
