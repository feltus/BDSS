"""link transfer reports and destinations

Revision ID: bc501eea2cfa
Revises: 69bd02aad8ae
Create Date: 2016-07-20 17:41:07.793003

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc501eea2cfa'
down_revision = '69bd02aad8ae'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('transfer_reports', sa.Column('destination_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'transfer_reports', 'destinations', ['destination_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'transfer_reports', type_='foreignkey')
    op.drop_column('transfer_reports', 'destination_id')
