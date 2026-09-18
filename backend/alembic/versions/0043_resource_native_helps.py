"""Add resource native help cache

Revision ID: 0043_resource_native_helps
Revises: 0042_reviews
Create Date: 2026-06-22
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0043_resource_native_helps"
down_revision: str | None = "0042_reviews"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "resource_native_helps",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("resource_type", sa.String(length=30), nullable=False),
        sa.Column("resource_key", sa.String(length=200), nullable=False),
        sa.Column("target_language", sa.String(length=10), nullable=False),
        sa.Column("native_language", sa.String(length=10), nullable=False),
        sa.Column("source_hash", sa.String(length=64), nullable=False),
        sa.Column("content", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "resource_type",
            "resource_key",
            "target_language",
            "native_language",
            name="uq_resource_native_helps_resource_lang",
        ),
    )
    op.create_index(
        "ix_resource_native_helps_lookup",
        "resource_native_helps",
        ["resource_type", "target_language"],
    )
    op.create_index(
        "ix_resource_native_helps_resource_type",
        "resource_native_helps",
        ["resource_type"],
    )
    op.create_index(
        "ix_resource_native_helps_resource_key",
        "resource_native_helps",
        ["resource_key"],
    )
    op.create_index(
        "ix_resource_native_helps_target_language",
        "resource_native_helps",
        ["target_language"],
    )
    op.create_index(
        "ix_resource_native_helps_native_language",
        "resource_native_helps",
        ["native_language"],
    )


def downgrade() -> None:
    op.drop_index("ix_resource_native_helps_native_language", table_name="resource_native_helps")
    op.drop_index("ix_resource_native_helps_target_language", table_name="resource_native_helps")
    op.drop_index("ix_resource_native_helps_resource_key", table_name="resource_native_helps")
    op.drop_index("ix_resource_native_helps_resource_type", table_name="resource_native_helps")
    op.drop_index("ix_resource_native_helps_lookup", table_name="resource_native_helps")
    op.drop_table("resource_native_helps")
