"""Multi-language support: user_languages table, study_plan_id columns, partial unique index

Revision ID: 0029_multi_language
Revises: 0028_trial_used
Create Date: 2026-06-02
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0029_multi_language"
down_revision: str | None = "0028_trial_used"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _add_study_plan_fk(
    table: str,
    constraint_name: str,
    ondelete: str,
) -> None:
    with op.batch_alter_table(table, recreate="auto") as batch_op:
        batch_op.create_foreign_key(
            constraint_name,
            "study_plans",
            ["study_plan_id"],
            ["id"],
            ondelete=ondelete,
        )


def _drop_study_plan_fk(table: str, constraint_name: str) -> None:
    with op.batch_alter_table(table, recreate="auto") as batch_op:
        batch_op.drop_constraint(constraint_name, type_="foreignkey")


def upgrade() -> None:
    # ── 1. Create user_languages table ──────────────────────────────────────
    op.create_table(
        "user_languages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("target_language", sa.String(10), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "target_language", name="uq_user_language"),
    )
    op.create_index("ix_user_languages_user_id", "user_languages", ["user_id"])
    op.create_index(
        "ix_user_language_user_active",
        "user_languages",
        ["user_id", "is_active"],
    )

    # ── 2. Add study_plan_id columns to 7 tables ────────────────────────────
    fk_specs = (
        ("progress", "fk_progress_study_plan", "CASCADE"),
        ("flashcards", "fk_flashcards_study_plan", "CASCADE"),
        ("user_competencies", "fk_user_competencies_study_plan", "CASCADE"),
        ("conversations", "fk_conversations_study_plan", "SET NULL"),
        ("chat_history", "fk_chat_history_study_plan", "SET NULL"),
        ("memories", "fk_memories_study_plan", "SET NULL"),
        ("llm_usage", "fk_llm_usage_study_plan", "SET NULL"),
    )

    for table, constraint_name, ondelete in fk_specs:
        op.add_column(table, sa.Column("study_plan_id", sa.Integer(), nullable=True))
        _add_study_plan_fk(table, constraint_name, ondelete)
        op.create_index(f"ix_{table}_study_plan_id", table, ["study_plan_id"])

    # ── 2.5. Deduplicate active plans before creating the unique index ─────
    # Keep the newest active plan for each (user_id, target_language).
    # The correlated subquery works on both PostgreSQL and SQLite.
    op.execute("""
        UPDATE study_plans
        SET is_active = false
        WHERE is_active = true
          AND id <> (
            SELECT keeper.id
            FROM study_plans AS keeper
            WHERE keeper.user_id = study_plans.user_id
              AND keeper.target_language = study_plans.target_language
              AND keeper.is_active = true
            ORDER BY keeper.created_at DESC, keeper.id DESC
            LIMIT 1
          )
        """)

    # ── 3. Partial unique index on study_plans ──────────────────────────────
    # Both dialects receive a real partial index predicate.
    op.create_index(
        "uq_active_plan_per_lang",
        "study_plans",
        ["user_id", "target_language"],
        unique=True,
        postgresql_where=sa.text("is_active = true"),
        sqlite_where=sa.text("is_active = 1"),
    )

    # ── 4. Data operations ──────────────────────────────────────────────────

    # 4a. Backfill user_languages from existing users.
    op.execute("""
        INSERT INTO user_languages (user_id, target_language, is_active, created_at)
        SELECT id, target_language, true, CURRENT_TIMESTAMP
        FROM users
        """)

    # 4b. Backfill study_plan_id for CASCADE tables.
    op.execute("""
        UPDATE progress
        SET study_plan_id = (
            SELECT sp.id
            FROM study_plans AS sp
            WHERE sp.user_id = progress.user_id
              AND sp.is_active = true
            ORDER BY sp.created_at DESC, sp.id DESC
            LIMIT 1
        )
        WHERE study_plan_id IS NULL
        """)
    op.execute("""
        UPDATE flashcards
        SET study_plan_id = (
            SELECT sp.id
            FROM study_plans AS sp
            WHERE sp.user_id = flashcards.user_id
              AND sp.is_active = true
            ORDER BY sp.created_at DESC, sp.id DESC
            LIMIT 1
        )
        WHERE study_plan_id IS NULL
        """)
    op.execute("""
        UPDATE user_competencies
        SET study_plan_id = (
            SELECT sp.id
            FROM study_plans AS sp
            WHERE sp.user_id = user_competencies.user_id
              AND sp.is_active = true
            ORDER BY sp.created_at DESC, sp.id DESC
            LIMIT 1
        )
        WHERE study_plan_id IS NULL
        """)

    # 4c. Create one fallback plan per user with orphaned rows and no active plan.
    # Plain GROUP BY and JSON text literals are portable across PostgreSQL/SQLite.
    for source_table in ("progress", "flashcards", "user_competencies"):
        op.execute(f"""
            INSERT INTO study_plans (
                user_id, cefr_level, target_language, goals,
                duration_weeks, days_per_week, current_unit, progress_day,
                generated_plan, is_active, completion_test_taken, created_at
            )
            SELECT source.user_id,
                   'A1',
                   COALESCE(u.target_language, 'en-US'),
                   '[]',
                   12,
                   4,
                   '',
                   0,
                   '{{}}',
                   true,
                   false,
                   CURRENT_TIMESTAMP
            FROM (
                SELECT user_id
                FROM {source_table}
                WHERE study_plan_id IS NULL
                GROUP BY user_id
            ) AS source
            JOIN users AS u ON u.id = source.user_id
            WHERE NOT EXISTS (
                SELECT 1
                FROM study_plans AS sp
                WHERE sp.user_id = source.user_id
                  AND sp.is_active = true
            )
            """)

    # 4d. Re-run backfill for rows whose fallback plan was just created.
    op.execute("""
        UPDATE progress
        SET study_plan_id = (
            SELECT sp.id
            FROM study_plans AS sp
            WHERE sp.user_id = progress.user_id
              AND sp.is_active = true
            ORDER BY sp.created_at DESC, sp.id DESC
            LIMIT 1
        )
        WHERE study_plan_id IS NULL
        """)
    op.execute("""
        UPDATE flashcards
        SET study_plan_id = (
            SELECT sp.id
            FROM study_plans AS sp
            WHERE sp.user_id = flashcards.user_id
              AND sp.is_active = true
            ORDER BY sp.created_at DESC, sp.id DESC
            LIMIT 1
        )
        WHERE study_plan_id IS NULL
        """)
    op.execute("""
        UPDATE user_competencies
        SET study_plan_id = (
            SELECT sp.id
            FROM study_plans AS sp
            WHERE sp.user_id = user_competencies.user_id
              AND sp.is_active = true
            ORDER BY sp.created_at DESC, sp.id DESC
            LIMIT 1
        )
        WHERE study_plan_id IS NULL
        """)


def downgrade() -> None:
    op.drop_index("uq_active_plan_per_lang", table_name="study_plans")

    fk_specs = (
        ("progress", "fk_progress_study_plan"),
        ("flashcards", "fk_flashcards_study_plan"),
        ("user_competencies", "fk_user_competencies_study_plan"),
        ("conversations", "fk_conversations_study_plan"),
        ("chat_history", "fk_chat_history_study_plan"),
        ("memories", "fk_memories_study_plan"),
        ("llm_usage", "fk_llm_usage_study_plan"),
    )

    for table, constraint_name in fk_specs:
        op.drop_index(f"ix_{table}_study_plan_id", table_name=table)
        _drop_study_plan_fk(table, constraint_name)
        with op.batch_alter_table(table, recreate="auto") as batch_op:
            batch_op.drop_column("study_plan_id")

    op.drop_index("ix_user_language_user_active", table_name="user_languages")
    op.drop_index("ix_user_languages_user_id", table_name="user_languages")
    op.drop_table("user_languages")
