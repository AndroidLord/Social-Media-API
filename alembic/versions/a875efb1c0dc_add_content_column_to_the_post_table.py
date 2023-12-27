"""add content column to the post table

Revision ID: a875efb1c0dc
Revises: 24f4534f8508
Create Date: 2023-12-25 17:12:46.331281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a875efb1c0dc'
down_revision: Union[str, None] = '24f4534f8508'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
