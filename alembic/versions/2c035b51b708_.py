"""empty message

Revision ID: 2c035b51b708
Revises: cd5e0d26eb97
Create Date: 2023-10-03 18:44:09.632662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c035b51b708'
down_revision = 'cd5e0d26eb97'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory_change_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity_change', sa.Integer(), nullable=False),
    sa.Column('new_quantity', sa.Integer(), nullable=False),
    sa.Column('change_timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_change_history_id'), 'inventory_change_history', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_inventory_change_history_id'), table_name='inventory_change_history')
    op.drop_table('inventory_change_history')
    # ### end Alembic commands ###
