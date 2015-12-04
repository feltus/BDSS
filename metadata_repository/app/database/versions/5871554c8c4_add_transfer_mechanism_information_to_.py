"""Add transfer mechanism information to data source

Revision ID: 5871554c8c4
Revises: 1ce8cdd4cdd
Create Date: 2015-12-04 11:19:55.775442

"""

# revision identifiers, used by Alembic.
revision = '5871554c8c4'
down_revision = '1ce8cdd4cdd'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from app.util import JSONEncodedDict


def upgrade():
    op.add_column('data_sources', sa.Column('transfer_mechanism_type', sa.String(length=100), nullable=False, server_default="curl"))
    op.add_column('data_sources', sa.Column('transfer_mechanism_options', JSONEncodedDict(), nullable=False, server_default="{}"))


def downgrade():
    op.drop_column('data_sources', 'transfer_mechanism_options')
    op.drop_column('data_sources', 'transfer_mechanism_type')
