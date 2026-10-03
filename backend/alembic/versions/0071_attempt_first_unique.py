"""One scored first attempt per user and reading/listening exercise.

Adds ``is_replay`` to reading_attempts and listening_attempts, marks existing
duplicate rows (everything except the earliest row per user and exercise) as
historical replays instead of deleting them, then enforces a partial unique
index on (user_id, exercise_id) for non-replay rows. Concurrent first
submissions can therefore no longer both persist and both award XP.
"""
from alembic import op
import sqlalchemy as sa

revision = "0071_attempt_first_unique"
down_revision = "0070_session_versions"
branch_labels = None
depends_on = None

_TABLES = (
    ("reading_attempts", "uq_reading_attempts_first_attempt"),
    ("listening_attempts", "uq_listening_attempts_first_attempt"),
)


def upgrade():
    for table_name, index_name in _TABLES:
        op.add_column(
            table_name,
            sa.Column("is_replay", sa.Boolean(), nullable=False, server_default=sa.false()),
        )
        table = sa.table(
            table_name,
            sa.column("id", sa.Integer()),
            sa.column("user_id", sa.Integer()),
            sa.column("exercise_id", sa.Integer()),
            sa.column("is_replay", sa.Boolean()),
        )
        first_ids = (
            sa.select(sa.func.min(table.c.id))
            .group_by(table.c.user_id, table.c.exercise_id)
        )
        op.execute(
            table.update()
            .where(table.c.id.not_in(first_ids))
            .values(is_replay=True)
        )
        op.create_index(
            index_name,
            table_name,
            ["user_id", "exercise_id"],
            unique=True,
            sqlite_where=sa.text("is_replay = 0"),
            postgresql_where=sa.text("is_replay = false"),
        )


def downgrade():
    for table_name, index_name in reversed(_TABLES):
        op.drop_index(index_name, table_name=table_name)
        with op.batch_alter_table(table_name) as table:
            table.drop_column("is_replay")
