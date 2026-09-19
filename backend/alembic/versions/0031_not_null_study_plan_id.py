"""Apply NOT NULL to study_plan_id (all callers now pass it)

Revision ID: 0031_not_null_study_plan_id
Revises: 0030_not_null_study_plan_id
Create Date: 2026-06-02
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0031_not_null_study_plan_id"
down_revision: str | None = "0030_not_null_study_plan_id"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    for table in ("progress", "flashcards", "user_competencies"):
        with op.batch_alter_table(table, recreate="auto") as batch_op:
            batch_op.alter_column("study_plan_id", nullable=False)


def downgrade() -> None:
    for table in ("user_competencies", "flashcards", "progress"):
        with op.batch_alter_table(table, recreate="auto") as batch_op:
            batch_op.alter_column("study_plan_id", nullable=True)
