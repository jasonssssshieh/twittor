"""add new column: is_activated

Revision ID: f9ee6c2620da
Revises: 2d08811c9dc8
Create Date: 2019-04-03 21:17:26.433206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9ee6c2620da'
down_revision = '2d08811c9dc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_activated', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_activated')
    # ### end Alembic commands ###
