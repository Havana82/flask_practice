"""created author model

Revision ID: 079bcb3c8b4c
Revises: a35319d745e0
Create Date: 2023-05-06 12:39:59.693900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '079bcb3c8b4c'
down_revision = 'a35319d745e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('author')
    # ### end Alembic commands ###
