"""add credential_updated_at on user

Revision ID: efe87f656855
Revises: a785a966dae9
Create Date: 2021-12-25 19:45:24.919168

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'efe87f656855'
down_revision = 'a785a966dae9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('credential_updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'credential_updated_at')
    # ### end Alembic commands ###
