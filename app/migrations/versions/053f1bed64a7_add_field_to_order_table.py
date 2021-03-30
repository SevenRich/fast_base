"""add field to order table

Revision ID: 053f1bed64a7
Revises: 26c6c1ed866f
Create Date: 2021-03-30 10:35:10.689580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '053f1bed64a7'
down_revision = '26c6c1ed866f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('batch_sn', sa.String(length=64), nullable=True, comment='码批次'))
    op.add_column('orders', sa.Column('export_config', sa.Text(), nullable=True, comment='导出码配置'))
    op.add_column('orders', sa.Column('export_key', sa.String(length=500), nullable=True, comment='导码密钥'))
    op.add_column('orders', sa.Column('url_prefix', sa.String(length=500), nullable=True, comment='Url 前缀'))
    op.alter_column('orders', 'code_config',
               existing_type=sa.TEXT(),
               comment='生码规则配置',
               existing_comment='码配置',
               existing_nullable=True)
    op.create_index(op.f('ix_orders_batch_sn'), 'orders', ['batch_sn'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_orders_batch_sn'), table_name='orders')
    op.alter_column('orders', 'code_config',
               existing_type=sa.TEXT(),
               comment='码配置',
               existing_comment='生码规则配置',
               existing_nullable=True)
    op.drop_column('orders', 'url_prefix')
    op.drop_column('orders', 'export_key')
    op.drop_column('orders', 'export_config')
    op.drop_column('orders', 'batch_sn')
    # ### end Alembic commands ###
