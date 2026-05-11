"""create messages table

Revision ID: 001
Revises:
Create Date: 2026-05-10

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "messages",
        sa.Column("message_id", UUID(as_uuid=True), primary_key=True),
        sa.Column("chat_id", UUID(as_uuid=True), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("rating", sa.Boolean(), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("role", sa.Enum("ai", "user", name="messagerole"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("messages")
    op.execute("DROP TYPE messagerole")
