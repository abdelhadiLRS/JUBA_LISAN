"""Invalidate old access/refresh sessions after password changes."""
from alembic import op
import sqlalchemy as sa

revision = "0070_session_versions"
down_revision = "0069_admin_bootstrap_claim"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("session_version", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("refresh_tokens", sa.Column("session_version", sa.Integer(), nullable=False, server_default="0"))


def downgrade():
    with op.batch_alter_table("refresh_tokens") as table:
        table.drop_column("session_version")
    with op.batch_alter_table("users") as table:
        table.drop_column("session_version")
