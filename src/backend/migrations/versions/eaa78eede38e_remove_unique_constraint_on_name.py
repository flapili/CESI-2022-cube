"""remove unique constraint on name

Revision ID: eaa78eede38e
Revises: 74007f075d2d
Create Date: 2021-12-21 10:58:49.425659

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'eaa78eede38e'
down_revision = '74007f075d2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('attachment_name_key', 'attachment', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('attachment_name_key', 'attachment', ['name'])
    # ### end Alembic commands ###