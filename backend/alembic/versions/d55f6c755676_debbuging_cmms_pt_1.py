"""debbuging CMMS pt.1

Revision ID: d55f6c755676
Revises: 918e436f746e
Create Date: 2025-11-11 12:14:01.891443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd55f6c755676'
down_revision: Union[str, Sequence[str], None] = '918e436f746e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
