"""add birthday

Revision ID: a785a966dae9
Revises: a2b3dcf59be9
Create Date: 2021-12-22 14:43:18.683820

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'a785a966dae9'
down_revision = 'a2b3dcf59be9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('birthday', sa.DateTime(timezone=True), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'birthday')
    # ### end Alembic commands ###
