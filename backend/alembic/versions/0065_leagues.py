"""Persist weekly language leagues and competition membership."""
import sqlalchemy as sa
from alembic import op

revision = "0065_leagues"
down_revision = "0064_merge_game_mistakes_and_user_languages"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "league_seasons",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("target_language", sa.String(10), nullable=False),
        sa.Column("week_start", sa.Date(), nullable=False),
        sa.Column("finalized", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.UniqueConstraint("target_language", "week_start", name="uq_league_language_week"),
    )
    op.create_table(
        "league_memberships",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("season_id", sa.Integer(), sa.ForeignKey("league_seasons.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("tier", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("joined_at", sa.DateTime(), nullable=False),
        sa.Column("final_xp", sa.Integer(), nullable=True),
        sa.Column("final_rank", sa.Integer(), nullable=True),
        sa.Column("next_tier", sa.Integer(), nullable=True),
        sa.UniqueConstraint("season_id", "user_id", name="uq_league_season_user"),
        sa.CheckConstraint("tier >= 0 AND tier <= 5", name="ck_league_tier"),
        sa.CheckConstraint("next_tier IS NULL OR (next_tier >= 0 AND next_tier <= 5)", name="ck_league_next_tier"),
    )
    op.create_index("ix_league_memberships_season_id", "league_memberships", ["season_id"])
    op.create_index("ix_league_memberships_user_id", "league_memberships", ["user_id"])
    op.create_index("ix_progress_date", "progress", ["date"])


def downgrade() -> None:
    op.drop_index("ix_progress_date", table_name="progress")
    op.drop_table("league_memberships")
    op.drop_table("league_seasons")
