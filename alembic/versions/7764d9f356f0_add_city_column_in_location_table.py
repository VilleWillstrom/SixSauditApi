"""add city column in location table

Revision ID: 7764d9f356f0
Revises: 
Create Date: 2023-12-31 23:08:18.329467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7764d9f356f0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tähän tulee se muutos mitä tähän halutaan tehdä
    op.add_column('location', sa.Column('city', sa.String(45)))
    pass


def downgrade() -> None:
    # Täällä halutaan kumota muutos
    # op.drop_column('location', 'city')
    pass
