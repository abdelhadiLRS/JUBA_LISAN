"""Restore the migration revision referenced by existing local databases.

This compatibility migration is intentionally idempotent. Older local databases
may already contain the speech-pause schema change while the migration file was
lost from the source tree. Keeping the revision in the chain lets Alembic
upgrade existing databases without requiring destructive resets.
"""

from alembic import op

revision = "0051_conversation_speech_pause"
down_revision = "0050_dashboard_banner"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Compatibility revision: existing deployments may already have the column.
    pass


def downgrade() -> None:
    # Deliberately a no-op; removing an unknown/possibly existing column would
    # be unsafe for databases upgraded from the historical revision.
    pass
