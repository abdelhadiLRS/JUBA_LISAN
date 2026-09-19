"""Add ondelete=CASCADE to FK constraints for user-owned tables

Revision ID: 0008_cascade_delete_user
Revises: 0007_target_language
Create Date: 2026-05-04
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0008_cascade_delete_user"
down_revision: str | None = "0007_target_language"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

FK_NAMING_CONVENTION = {"fk": "%(table_name)s_%(column_0_name)s_fkey"}


def _replace_fk(
    table: str,
    constraint_name: str,
    referred_table: str,
    local_cols: list[str],
    referred_cols: list[str],
    *,
    ondelete: str | None,
) -> None:
    # The initial SQLite schema contains unnamed foreign keys. Supplying a
    # naming convention lets Alembic assign stable names while reflecting
    # those existing constraints, so the same migration works on SQLite and
    # databases that already have convention-based FK names.
    with op.batch_alter_table(
        table,
        recreate="auto",
        naming_convention=FK_NAMING_CONVENTION,
    ) as batch_op:
        batch_op.drop_constraint(constraint_name, type_="foreignkey")
        batch_op.create_foreign_key(
            constraint_name,
            referred_table,
            local_cols,
            referred_cols,
            ondelete=ondelete,
        )


def upgrade() -> None:
    constraints = (
        ("flashcards", "flashcards_user_id_fkey", "users", ["user_id"], ["id"]),
        ("study_plans", "study_plans_user_id_fkey", "users", ["user_id"], ["id"]),
        ("progress", "progress_user_id_fkey", "users", ["user_id"], ["id"]),
        ("chat_history", "chat_history_user_id_fkey", "users", ["user_id"], ["id"]),
        ("lessons", "lessons_study_plan_id_fkey", "study_plans", ["study_plan_id"], ["id"]),
        ("exercises", "exercises_lesson_id_fkey", "lessons", ["lesson_id"], ["id"]),
    )

    for table, constraint_name, referred_table, local_cols, referred_cols in constraints:
        _replace_fk(
            table,
            constraint_name,
            referred_table,
            local_cols,
            referred_cols,
            ondelete="CASCADE",
        )


def downgrade() -> None:
    constraints = (
        ("exercises", "exercises_lesson_id_fkey", "lessons", ["lesson_id"], ["id"]),
        ("lessons", "lessons_study_plan_id_fkey", "study_plans", ["study_plan_id"], ["id"]),
        ("chat_history", "chat_history_user_id_fkey", "users", ["user_id"], ["id"]),
        ("progress", "progress_user_id_fkey", "users", ["user_id"], ["id"]),
        ("study_plans", "study_plans_user_id_fkey", "users", ["user_id"], ["id"]),
        ("flashcards", "flashcards_user_id_fkey", "users", ["user_id"], ["id"]),
    )

    for table, constraint_name, referred_table, local_cols, referred_cols in constraints:
        _replace_fk(
            table,
            constraint_name,
            referred_table,
            local_cols,
            referred_cols,
            ondelete=None,
        )
