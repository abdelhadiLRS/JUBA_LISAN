"""Add user_language_id FK to study_plans for referential integrity

Revision ID: 0034_user_language_id_fk
Revises: 0033_progress_unique_constraint
Create Date: 2026-06-05
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0034_user_language_id_fk"
down_revision: str | None = "0033_progress_unique_constraint"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("study_plans", sa.Column("user_language_id", sa.Integer(), nullable=True))

    with op.batch_alter_table("study_plans", recreate="auto") as batch_op:
        batch_op.create_foreign_key(
            "fk_study_plans_user_language",
            "user_languages",
            ["user_language_id"],
            ["id"],
            ondelete="CASCADE",
        )
    op.create_index(
        "ix_study_plans_user_language_id",
        "study_plans",
        ["user_language_id"],
    )

    op.execute("""
        INSERT INTO user_languages (user_id, target_language, is_active, created_at)
        SELECT sp.user_id, sp.target_language, false, CURRENT_TIMESTAMP
        FROM study_plans AS sp
        WHERE NOT EXISTS (
            SELECT 1
            FROM user_languages AS ul
            WHERE ul.user_id = sp.user_id
              AND ul.target_language = sp.target_language
        )
        """)

    op.execute("""
        UPDATE study_plans
        SET user_language_id = (
            SELECT ul.id
            FROM user_languages AS ul
            WHERE ul.user_id = study_plans.user_id
              AND ul.target_language = study_plans.target_language
            ORDER BY ul.id
            LIMIT 1
        )
        WHERE user_language_id IS NULL
        """)

    op.drop_index("uq_active_plan_per_lang", table_name="study_plans")
    op.create_index(
        "uq_active_plan_per_lang",
        "study_plans",
        ["user_language_id"],
        unique=True,
        postgresql_where=sa.text("is_active = true"),
        sqlite_where=sa.text("is_active = 1"),
    )

    with op.batch_alter_table("study_plans", recreate="auto") as batch_op:
        batch_op.alter_column("user_language_id", nullable=False)


def downgrade() -> None:
    op.drop_index("uq_active_plan_per_lang", table_name="study_plans")
    op.drop_index("ix_study_plans_user_language_id", table_name="study_plans")

    with op.batch_alter_table("study_plans", recreate="auto") as batch_op:
        batch_op.drop_constraint(
            "fk_study_plans_user_language",
            type_="foreignkey",
        )
        batch_op.drop_column("user_language_id")

    op.create_index(
        "uq_active_plan_per_lang",
        "study_plans",
        ["user_id", "target_language"],
        unique=True,
        postgresql_where=sa.text("is_active = true"),
        sqlite_where=sa.text("is_active = 1"),
    )
