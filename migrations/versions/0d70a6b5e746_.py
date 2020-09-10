"""empty message

Revision ID: 0d70a6b5e746
Revises: a0f15e5111fa
Create Date: 2020-09-10 14:39:04.229293

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0d70a6b5e746'
down_revision = 'a0f15e5111fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'age')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('age', mysql.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
