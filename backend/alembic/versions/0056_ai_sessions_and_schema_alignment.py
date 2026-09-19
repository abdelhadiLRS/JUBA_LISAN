"""Align model metadata with the database schema and add AI tutor sessions.

Revision ID: 0056_ai_sessions_and_schema_alignment
Revises: 0055_game_sessions
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0056_ai_sessions_and_schema_alignment"
down_revision: str | None = "0055_game_sessions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # The uniqueness is already enforced by the table-level constraints created
    # by the original migrations. The ORM does not need a second redundant index.
    op.drop_index("ix_reviews_user_id", table_name="reviews")
    op.drop_index("ix_users_username", table_name="users")

    op.create_table(
        "ai_sessions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("language", sa.String(length=10), nullable=False),
        sa.Column("topic", sa.String(length=255), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "ACTIVE",
                "COMPLETED",
                "CANCELLED",
                name="sessionstatus",
            ),
            nullable=False,
        ),
        sa.Column("total_messages", sa.Integer(), nullable=False),
        sa.Column("duration_seconds", sa.Integer(), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_sessions_user_id", "ai_sessions", ["user_id"], unique=False)

    op.create_table(
        "speech_analyses",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("audio_url", sa.Text(), nullable=True),
        sa.Column("transcription", sa.Text(), nullable=True),
        sa.Column("expected_text", sa.Text(), nullable=True),
        sa.Column("pronunciation_score", sa.Float(), nullable=True),
        sa.Column("fluency_score", sa.Float(), nullable=True),
        sa.Column("accuracy_score", sa.Float(), nullable=True),
        sa.Column(
            "overall_quality",
            sa.Enum(
                "EXCELLENT",
                "GOOD",
                "FAIR",
                "NEEDS_IMPROVEMENT",
                name="speechquality",
            ),
            nullable=True,
        ),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("phoneme_errors", sa.Text(), nullable=True),
        sa.Column("analyzed_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["ai_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_speech_analyses_session_id",
        "speech_analyses",
        ["session_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_speech_analyses_session_id", table_name="speech_analyses")
    op.drop_table("speech_analyses")
    op.drop_index("ix_ai_sessions_user_id", table_name="ai_sessions")
    op.drop_table("ai_sessions")

    # PostgreSQL stores SQLAlchemy enums as named types; remove them on downgrade
    # so the migration can be applied again cleanly.
    if op.get_bind().dialect.name == "postgresql":
        op.execute("DROP TYPE IF EXISTS speechquality")
        op.execute("DROP TYPE IF EXISTS sessionstatus")

    op.create_index("ix_reviews_user_id", "reviews", ["user_id"], unique=False)
    op.create_index("ix_users_username", "users", ["username"], unique=False)
