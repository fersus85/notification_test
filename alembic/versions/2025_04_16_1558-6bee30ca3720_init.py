"""Init

Revision ID: 6bee30ca3720
Revises:
Create Date: 2025-04-16 15:58:50.120291

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6bee30ca3720"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notifications",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "read_at", postgresql.TIMESTAMP(timezone=True), nullable=True
        ),
        sa.Column(
            "category",
            sa.Enum(
                "INFO", "WARNING", "CRITICAL", name="notification_category"
            ),
            nullable=True,
        ),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column(
            "processing_status",
            sa.Enum(
                "PENDING",
                "PROCESSING",
                "COMPLETED",
                "FAILED",
                name="notification_processing_status",
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_notifications_category"),
        "notifications",
        ["category"],
        unique=False,
    )
    op.create_index(
        op.f("ix_notifications_processing_status"),
        "notifications",
        ["processing_status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_notifications_user_id"),
        "notifications",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_notifications_user_status_created",
        "notifications",
        ["user_id", "processing_status", "created_at"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "ix_notifications_user_status_created", table_name="notifications"
    )
    op.drop_index(op.f("ix_notifications_user_id"), table_name="notifications")
    op.drop_index(
        op.f("ix_notifications_processing_status"), table_name="notifications"
    )
    op.drop_index(
        op.f("ix_notifications_category"), table_name="notifications"
    )
    op.drop_table("notifications")
    # ### end Alembic commands ###
