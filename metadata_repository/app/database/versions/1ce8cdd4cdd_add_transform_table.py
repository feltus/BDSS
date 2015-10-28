"""Add transform table.

Revision ID: 1ce8cdd4cdd
Revises: 172452fedc5
Create Date: 2015-10-28 15:59:59.562683

"""

# revision identifiers, used by Alembic.
revision = '1ce8cdd4cdd'
down_revision = '172452fedc5'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from app.util import JSONEncodedDict


def upgrade():
    op.create_table('url_transforms',
        sa.Column('transform_id', sa.Integer(), nullable=False),
        sa.Column('from_data_source_id', sa.Integer(), nullable=False),
        sa.Column('to_data_source_id', sa.Integer(), nullable=False),
        sa.Column('transform_type', sa.String(length=100), nullable=False),
        sa.Column('transform_options', JSONEncodedDict(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['from_data_source_id'], ['data_sources.id'], ),
        sa.ForeignKeyConstraint(['to_data_source_id'], ['data_sources.id'], ),
        sa.PrimaryKeyConstraint('transform_id', 'from_data_source_id'),
        sqlite_autoincrement=True
    )


def downgrade():
    op.drop_table('url_transforms')
