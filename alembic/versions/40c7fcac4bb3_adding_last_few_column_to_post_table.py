"""adding last few column to post table

Revision ID: 40c7fcac4bb3
Revises: 642e64807515
Create Date: 2023-12-25 18:00:27.293835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40c7fcac4bb3'
down_revision: Union[str, None] = '642e64807515'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column('posts', sa.Column('published', sa.Boolean,

                                     server_default='True', nullable=False))

    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                     server_default=sa.text('now()'), nullable=False))

    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
