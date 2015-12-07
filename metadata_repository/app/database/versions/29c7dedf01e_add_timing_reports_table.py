"""Add timing reports table

Revision ID: 29c7dedf01e
Revises: 5871554c8c4
Create Date: 2015-12-07 09:49:20.140599

"""

# revision identifiers, used by Alembic.
revision = '29c7dedf01e'
down_revision = '5871554c8c4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('timing_reports',
                    sa.Column('report_id', sa.Integer(), nullable=False),
                    sa.Column('data_source_id', sa.Integer(), nullable=False),
                    sa.Column('url', sa.Text(), nullable=False),
                    sa.Column('file_size_bytes', sa.Integer(), nullable=False),
                    sa.Column('transfer_duration_seconds', sa.Float(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['data_source_id'], ['data_sources.id'], ),
                    sa.PrimaryKeyConstraint('report_id', 'data_source_id'))


def downgrade():
    op.drop_table('timing_reports')
