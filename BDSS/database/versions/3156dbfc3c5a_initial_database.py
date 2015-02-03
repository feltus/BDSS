"""Initial database

Revision ID: 3156dbfc3c5a
Revises:
Create Date: 2015-02-03 12:41:55.066202

"""

# revision identifiers, used by Alembic.
revision = '3156dbfc3c5a'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():

    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=50), nullable=False),
        sa.Column('password_hash', sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    op.create_table('ssh_keys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('destination', sa.String(length=100), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('public', sa.Text(), nullable=False),
        sa.Column('private', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('owner_id', 'destination', name='_duplicate_keys_constraint')
    )

    op.create_table('jobs',
        sa.Column('job_id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('data_transfer_method', sa.String(length=30), nullable=False),
        sa.Column('_data_transfer_method_options', sa.Text(), nullable=False),
        sa.Column('data_destination', sa.String(length=30), nullable=False),
        sa.Column('destination_directory', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('measured_time', sa.Float(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('reporting_token', sa.String(length=32), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('job_id')
    )

    op.create_table('data_items',
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('job_id', sa.Integer(), nullable=False),
        sa.Column('data_url', sa.String(length=200), nullable=False),
        sa.Column('checksum', sa.String(length=64), nullable=True),
        sa.Column('checksum_method', sa.Enum('md5', name='checksum_methods'), nullable=True),
        sa.Column('group', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('transfer_started_at', sa.DateTime(), nullable=True),
        sa.Column('transfer_finished_at', sa.DateTime(), nullable=True),
        sa.Column('measured_transfer_time', sa.Float(), nullable=True),
        sa.Column('transfer_size', sa.BigInteger(), nullable=True),
        sa.Column('status', sa.Enum('pending', 'in_progress', 'completed', 'failed', name='data_transfer_statuses'), nullable=False),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.job_id'], ),
        sa.PrimaryKeyConstraint('item_id'),
        sa.UniqueConstraint('job_id', 'data_url', name='_duplicate_urls_constraint')
    )


def downgrade():
    op.drop_table('data_items')
    op.drop_table('jobs')
    op.drop_table('ssh_keys')
    op.drop_table('users')
