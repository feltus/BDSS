"""First tables.

Revision ID: 172452fedc5
Revises:
Create Date: 2015-10-27 16:33:58.486789

"""

# revision identifiers, used by Alembic.
revision = '172452fedc5'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from app.util import JSONEncodedDict


def upgrade():
    op.create_table('data_sources',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('label', sa.String(length=100), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'))
    op.create_table('url_matchers',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('data_source_id', sa.Integer(), nullable=False),
                    sa.Column('matcher_type', sa.String(length=100), nullable=False),
                    sa.Column('matcher_options', JSONEncodedDict(), nullable=False, server_default="{}"),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['data_source_id'], ['data_sources.id'], ),
                    sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('url_matchers')
    op.drop_table('data_sources')
