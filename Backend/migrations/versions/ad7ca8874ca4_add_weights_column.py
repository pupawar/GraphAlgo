"""Add weights column

Revision ID: ad7ca8874ca4
Revises: 
Create Date: 2024-11-12 15:23:34.679284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad7ca8874ca4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('edges', schema=None) as batch_op:
        batch_op.add_column(sa.Column('weight', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('edges', schema=None) as batch_op:
        batch_op.drop_column('weight')

    # ### end Alembic commands ###
