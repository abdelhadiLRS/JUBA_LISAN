"""Durable atomic first-admin bootstrap, without changing existing roles."""
from alembic import op
import sqlalchemy as sa

revision = "0069_admin_bootstrap_claim"
down_revision = "0068_billing_intents"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "admin_bootstrap_claims",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=False),
        sa.CheckConstraint("id = 1", name="ck_admin_bootstrap_singleton"),
    )
    # Existing installations have already passed first-user bootstrap. Never
    # promote anybody or re-enable bootstrap if their users are later deleted.
    op.execute(sa.text(
        "INSERT INTO admin_bootstrap_claims (id) "
        "SELECT 1 WHERE EXISTS (SELECT 1 FROM users)"
    ))


def downgrade() -> None:
    op.drop_table("admin_bootstrap_claims")
