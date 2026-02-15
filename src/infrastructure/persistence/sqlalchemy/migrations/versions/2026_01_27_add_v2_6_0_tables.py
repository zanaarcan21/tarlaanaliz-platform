# BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

"""add v2.6.0 tables

Revision ID: 2026_01_27_add_v2_6_0_tables
Revises:
Create Date: 2026-01-27
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "2026_01_27_add_v2_6_0_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # KR-081: AnalysisJob contract-first persistence tablosu.
    # KR-018: Kalibrasyon hard-gate durumu kalıcı olarak tutulur.
    op.create_table(
        "analysis_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("mission_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("schema_version", sa.String(length=32), nullable=False),
        sa.Column("input_payload_uri", sa.Text(), nullable=False),
        sa.Column("output_payload_uri", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="queued"),
        sa.Column(
            "calibration_gate_passed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_analysis_jobs_mission_id",
        "analysis_jobs",
        ["mission_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_analysis_jobs_mission_id", table_name="analysis_jobs")
    op.drop_table("analysis_jobs")
