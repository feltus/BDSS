"""Add test files table

Revision ID: 15f5bf79bb0
Revises: 29c7dedf01e
Create Date: 2015-12-07 11:09:53.702970

"""

# revision identifiers, used by Alembic.
revision = '15f5bf79bb0'
down_revision = '29c7dedf01e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('transfer_test_files',
                    sa.Column('file_id', sa.Integer(), nullable=False),
                    sa.Column('data_source_id', sa.Integer(), nullable=False),
                    sa.Column('url', sa.Text(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['data_source_id'], ['data_sources.id'], ),
                    sa.PrimaryKeyConstraint('file_id', 'data_source_id'))


def downgrade():
    op.drop_table('transfer_test_files')
