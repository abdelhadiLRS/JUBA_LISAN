"""Align study plans with the multi-language learning model.

Revision ID: 0063_user_languages_and_plan_scope
Revises: 0062_progress_reward_xp
"""
from collections.abc import Sequence
from datetime import datetime

import sqlalchemy as sa
from alembic import op

revision: str = "0063_user_languages_and_plan_scope"
down_revision: str | None = "0062_progress_reward_xp"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "user_languages" not in inspector.get_table_names():
        op.create_table(
            "user_languages",
            sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("target_language", sa.String(10), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.UniqueConstraint("user_id", "target_language", name="uq_user_language"),
        )
        op.create_index("ix_user_language_user_id", "user_languages", ["user_id"])
        op.create_index("ix_user_language_user_active", "user_languages", ["user_id", "is_active"])

    users = sa.table(
        "users",
        sa.column("id", sa.Integer()),
        sa.column("target_language", sa.String(10)),
    )
    languages = sa.table(
        "user_languages",
        sa.column("id", sa.Integer()),
        sa.column("user_id", sa.Integer()),
        sa.column("target_language", sa.String(10)),
        sa.column("is_active", sa.Boolean()),
        sa.column("created_at", sa.DateTime()),
    )

    existing = {
        (row[0], row[1])
        for row in bind.execute(sa.select(languages.c.user_id, languages.c.target_language)).all()
    }
    for row in bind.execute(sa.select(users.c.id, users.c.target_language)).all():
        key = (row[0], row[1] or "en-US")
        if key not in existing:
            bind.execute(
                languages.insert().values(
                    user_id=key[0],
                    target_language=key[1],
                    is_active=True,
                    created_at=datetime.utcnow(),
                )
            )

    inspector = sa.inspect(bind)
    plan_columns = {column["name"] for column in inspector.get_columns("study_plans")}
    if "user_language_id" not in plan_columns:
        op.add_column(
            "study_plans",
            sa.Column("user_language_id", sa.Integer(), nullable=True),
        )

    op.execute(
        sa.text(
            """
            UPDATE study_plans
            SET user_language_id = (
                SELECT ul.id
                FROM user_languages ul
                JOIN users u ON u.id = ul.user_id
                WHERE ul.user_id = study_plans.user_id
                  AND ul.target_language = COALESCE(u.target_language, 'en-US')
                ORDER BY ul.id
                LIMIT 1
            )
            WHERE user_language_id IS NULL
            """
        )
    )

    with op.batch_alter_table("study_plans", recreate="auto") as batch_op:
        batch_op.alter_column("user_language_id", nullable=False)
        batch_op.create_foreign_key(
            "fk_study_plans_user_language_id",
            "user_languages",
            ["user_language_id"],
            ["id"],
            ondelete="CASCADE",
        )

    if bind.dialect.name == "sqlite":
        op.create_index(
            "uq_active_plan_per_lang",
            "study_plans",
            ["user_language_id"],
            unique=True,
            sqlite_where=sa.text("is_active = 1"),
        )
    elif bind.dialect.name == "postgresql":
        op.create_index(
            "uq_active_plan_per_lang",
            "study_plans",
            ["user_language_id"],
            unique=True,
            postgresql_where=sa.text("is_active = true"),
        )
    else:
        op.create_index(
            "ix_study_plans_user_language_id",
            "study_plans",
            ["user_language_id"],
        )


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name in {"sqlite", "postgresql"}:
        op.drop_index("uq_active_plan_per_lang", table_name="study_plans")
    else:
        op.drop_index("ix_study_plans_user_language_id", table_name="study_plans")
    with op.batch_alter_table("study_plans", recreate="auto") as batch_op:
        batch_op.drop_constraint("fk_study_plans_user_language_id", type_="foreignkey")
        batch_op.drop_column("user_language_id")
    op.drop_index("ix_user_language_user_active", table_name="user_languages")
    op.drop_index("ix_user_language_user_id", table_name="user_languages")
    op.drop_table("user_languages")
