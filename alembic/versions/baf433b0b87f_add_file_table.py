"""add file table

Revision ID: baf433b0b87f
Revises: 7764d9f356f0
Create Date: 2023-12-31 23:25:25.706747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'baf433b0b87f'
down_revision: Union[str, None] = '7764d9f356f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('file',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('original_name', sa.String(255), nullable=False),
                    sa.Column('random_name', sa.String(255),nullable=False, unique=True),
                    # Following is for ForeignKeys to manage relations
                    sa.Column('inspectionform_id', sa.Integer, nullable=False, index=True),
                    sa.ForeignKeyConstraint(('inspectionform_id', ), ['inspectionform.id']))


def downgrade() -> None:
    # What happens when downgrading from this revision
    op.drop_table('file')
