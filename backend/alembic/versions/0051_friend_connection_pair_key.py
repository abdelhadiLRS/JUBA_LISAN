"""Enforce one canonical friendship row per learner pair.

Revision ID: 0051_friend_connection_pair_key
Revises: 0050_learning_social
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0051_friend_connection_pair_key"
down_revision: str | None = "0050_learning_social"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("friend_connections", recreate="auto") as batch_op:
        batch_op.add_column(sa.Column("pair_key", sa.String(length=40), nullable=True))

    op.execute("""
        UPDATE friend_connections
        SET pair_key = CASE
            WHEN requester_id < addressee_id
                THEN CAST(requester_id AS TEXT) || ':' || CAST(addressee_id AS TEXT)
            ELSE CAST(addressee_id AS TEXT) || ':' || CAST(requester_id AS TEXT)
        END
    """)

    # Keep the oldest row if legacy data ever contains both directions.
    op.execute("""
        DELETE FROM friend_connections
        WHERE id IN (
            SELECT newer.id
            FROM friend_connections AS newer
            JOIN friend_connections AS older
              ON newer.pair_key = older.pair_key AND older.id < newer.id
        )
    """)

    with op.batch_alter_table("friend_connections", recreate="auto") as batch_op:
        batch_op.alter_column("pair_key", nullable=False)
        batch_op.create_unique_constraint(
            "uq_friend_connection_pair_key", ["pair_key"]
        )
        batch_op.create_index("ix_friend_connections_pair_key", ["pair_key"])


def downgrade() -> None:
    with op.batch_alter_table("friend_connections", recreate="auto") as batch_op:
        batch_op.drop_index("ix_friend_connections_pair_key")
        batch_op.drop_constraint(
            "uq_friend_connection_pair_key", type_="unique"
        )
        batch_op.drop_column("pair_key")
