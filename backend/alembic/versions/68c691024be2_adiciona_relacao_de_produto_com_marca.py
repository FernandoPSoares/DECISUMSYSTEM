"""Adiciona relacao de produto com marca

Revision ID: 68c691024be2
Revises: 6f0b7c53e90d
Create Date: 2025-10-21 15:31:50.323451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68c691024be2'
down_revision: Union[str, Sequence[str], None] = '6f0b7c53e90d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
