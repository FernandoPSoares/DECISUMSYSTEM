"""Adiciona modulos de CMMS (Equipes, Ativos, OSs, PMs)

Revision ID: 918e436f746e
Revises: 68c691024be2
Create Date: 2025-11-11 11:47:51.335817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '918e436f746e'
down_revision: Union[str, Sequence[str], None] = '68c691024be2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
