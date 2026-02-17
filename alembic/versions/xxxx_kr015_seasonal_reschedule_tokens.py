"""KR-015: seasonal reschedule tokens + reschedule requests (scaffold)

Rename file with real timestamp prefix per your convention.
"""

from alembic import op
import sqlalchemy as sa

revision = "xxxx_kr015_seasonal_reschedule_tokens"
down_revision = None  # TODO
branch_labels = None
depends_on = None


def upgrade() -> None:
    # subscriptions token fields
    op.add_column("subscriptions", sa.Column("plan_type", sa.String(length=32), nullable=True))
    op.add_column("subscriptions", sa.Column("reschedule_tokens_per_season", sa.Integer(), nullable=True))
    op.add_column("subscriptions", sa.Column("reschedule_tokens_remaining", sa.Integer(), nullable=True))

    # reschedule request table
    op.create_table(
        "subscription_reschedule_requests",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("subscription_id", sa.String(length=36), nullable=False, index=True),
        sa.Column("mission_id", sa.String(length=36), nullable=True, index=True),
        sa.Column("occurrence_ref", sa.String(length=64), nullable=True),
        sa.Column("requested_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("requested_by", sa.String(length=36), nullable=False),
        sa.Column("reviewed_by", sa.String(length=36), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("subscription_reschedule_requests")
    op.drop_column("subscriptions", "reschedule_tokens_remaining")
    op.drop_column("subscriptions", "reschedule_tokens_per_season")
    op.drop_column("subscriptions", "plan_type")
