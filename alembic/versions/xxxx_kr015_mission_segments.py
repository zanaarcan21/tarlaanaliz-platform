"""KR-015 (optional): mission_segments table (scaffold)

Rename file with real timestamp prefix per your convention.
"""

from alembic import op
import sqlalchemy as sa

revision = "xxxx_kr015_mission_segments"
down_revision = None  # TODO
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "mission_segments",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("mission_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("segment_no", sa.Integer(), nullable=False),
        sa.Column("area_donum", sa.Integer(), nullable=False),
        sa.Column("assigned_pilot_id", sa.String(length=36), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PLANNED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_table("mission_segments")
