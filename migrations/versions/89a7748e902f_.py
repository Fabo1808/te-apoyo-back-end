"""empty message

Revision ID: 89a7748e902f
Revises: e5b0082e8dba
Create Date: 2021-11-08 16:18:57.033406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89a7748e902f'
down_revision = 'e5b0082e8dba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ong', sa.Column('account', sa.String(length=30), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ong', 'account')
    # ### end Alembic commands ###