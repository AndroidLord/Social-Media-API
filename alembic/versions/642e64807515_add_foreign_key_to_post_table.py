"""add foreign key to post table

Revision ID: 642e64807515
Revises: 5bb3c946ee26
Create Date: 2023-12-25 17:53:30.328273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '642e64807515'
down_revision: Union[str, None] = '5bb3c946ee26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key('post_user_fk',
                          source_table= 'posts', referent_table='users',
                          local_cols = ['owner_id'], remote_cols = ['id'],
                          ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
