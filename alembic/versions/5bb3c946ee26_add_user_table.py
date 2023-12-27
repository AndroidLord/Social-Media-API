"""add user table

Revision ID: 5bb3c946ee26
Revises: a875efb1c0dc
Create Date: 2023-12-25 17:26:05.211920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bb3c946ee26'
down_revision: Union[str, None] = 'a875efb1c0dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
