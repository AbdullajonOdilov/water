"""Initial migration

Revision ID: 993888c35e25
Revises: abc3d5eb8c8c
Create Date: 2023-08-12 12:50:16.601155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '993888c35e25'
down_revision = 'abc3d5eb8c8c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('file', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'file')
    # ### end Alembic commands ###