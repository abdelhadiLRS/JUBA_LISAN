"""Enforce globally unique memory content per user.

Revision ID: 0049_memory_user_content_unique
Revises: 0048_cancel_at_period_end
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0049_memory_user_content_unique"
down_revision: str | None = "0048_cancel_at_period_end"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        DELETE FROM memories
        WHERE EXISTS (
            SELECT 1
            FROM memories AS older
            WHERE older.user_id = memories.user_id
              AND older.content = memories.content
              AND older.id < memories.id
        )
    """)

    with op.batch_alter_table("memories", recreate="auto") as batch_op:
        batch_op.create_unique_constraint(
            "uq_memories_user_content",
            ["user_id", "content"],
        )


def downgrade() -> None:
    with op.batch_alter_table("memories", recreate="auto") as batch_op:
        batch_op.drop_constraint("uq_memories_user_content", type_="unique")
