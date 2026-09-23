"""Add learner friendships and direct messages.

Revision ID: 0050_learning_social
Revises: 0049_memory_user_content_unique
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0050_learning_social"
down_revision: str | None = "0049_memory_user_content_unique"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "friend_connections",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("requester_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("addressee_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("requester_id", "addressee_id", name="uq_friend_connection_pair"),
    )
    op.create_index("ix_friend_connections_requester_id", "friend_connections", ["requester_id"])
    op.create_index("ix_friend_connections_addressee_id", "friend_connections", ["addressee_id"])
    op.create_index("ix_friend_connections_status", "friend_connections", ["status"])

    op.create_table(
        "direct_messages",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("sender_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("recipient_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_direct_messages_sender_id", "direct_messages", ["sender_id"])
    op.create_index("ix_direct_messages_recipient_id", "direct_messages", ["recipient_id"])
    op.create_index("ix_direct_messages_created_at", "direct_messages", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_direct_messages_created_at", table_name="direct_messages")
    op.drop_index("ix_direct_messages_recipient_id", table_name="direct_messages")
    op.drop_index("ix_direct_messages_sender_id", table_name="direct_messages")
    op.drop_table("direct_messages")
    op.drop_index("ix_friend_connections_status", table_name="friend_connections")
    op.drop_index("ix_friend_connections_addressee_id", table_name="friend_connections")
    op.drop_index("ix_friend_connections_requester_id", table_name="friend_connections")
    op.drop_table("friend_connections")
