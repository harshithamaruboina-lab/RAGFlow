"""add chunk embeddings

Revision ID: dd939bd228e2
Revises: d285fa98b4b0
Create Date: 2026-08-01 16:43:42.437910+00:00
"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision = "dd939bd228e2"
down_revision = "d285fa98b4b0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "document_chunks",
        sa.Column(
            "embedding",
            Vector(384),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "document_chunks",
        "embedding",
    )