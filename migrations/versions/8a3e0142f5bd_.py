"""empty message

Revision ID: 8a3e0142f5bd
Revises: ecc983704af9
Create Date: 2020-07-09 21:56:25.369769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a3e0142f5bd'
down_revision = 'ecc983704af9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'important',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'important',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
