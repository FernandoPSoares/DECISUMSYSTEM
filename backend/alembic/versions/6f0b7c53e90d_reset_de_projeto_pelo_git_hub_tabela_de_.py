"""Reset de projeto pelo git hub + tabela de Marcas (brand)

Revision ID: 6f0b7c53e90d
Revises: 832080cd91ad
Create Date: 2025-10-21 15:27:07.653748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f0b7c53e90d'
down_revision: Union[str, Sequence[str], None] = '832080cd91ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
