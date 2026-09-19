"""Add unique constraint on user_competencies to prevent duplicates per plan

Revision ID: 0035_competency_unique
Revises: 0034_user_language_id_fk
Create Date: 2026-06-05
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0035_competency_unique"
down_revision: str | None = "0034_user_language_id_fk"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        DELETE FROM user_competencies
        WHERE EXISTS (
            SELECT 1
            FROM user_competencies AS keeper
            WHERE keeper.user_id = user_competencies.user_id
              AND keeper.study_plan_id = user_competencies.study_plan_id
              AND keeper.unit_id = user_competencies.unit_id
              AND keeper.competency_text = user_competencies.competency_text
              AND keeper.id < user_competencies.id
        )
    """)

    with op.batch_alter_table("user_competencies", recreate="auto") as batch_op:
        batch_op.create_unique_constraint(
            "uq_competency_user_plan_unit_text",
            ["user_id", "study_plan_id", "unit_id", "competency_text"],
        )


def downgrade() -> None:
    with op.batch_alter_table("user_competencies", recreate="auto") as batch_op:
        batch_op.drop_constraint("uq_competency_user_plan_unit_text", type_="unique")
