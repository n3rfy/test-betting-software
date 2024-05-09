"""Add event and bet table

Revision ID: 0e8e829978c7
Revises: 
Create Date: 2024-05-09 12:55:51.835724

"""
import sqlalchemy as sa
from alembic import op


revision = '0e8e829978c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'event',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'WIN', 'LOSE', name='eventstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'bet',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('event_id', sa.UUID(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('bet')
    op.drop_table('event')
