"""Added enum for order status

Revision ID: 95208a4e4685
Revises: 0159498f8d9b
Create Date: 2024-09-29 21:58:13.039504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '95208a4e4685'
down_revision: Union[str, None] = '0159498f8d9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

order_status_enum = postgresql.ENUM(
    'in_process', 'shipping', 'delivered', name='orderstatus')


def upgrade() -> None:
    order_status_enum.create(op.get_bind())
    op.execute("""
        UPDATE orders
        SET status = 'in_process' WHERE status = 'в процессе';
        UPDATE orders
        SET status = 'shipping' WHERE status = 'отправлен';
        UPDATE orders
        SET status = 'delivered' WHERE status = 'доставлен';
    """)
    op.execute(
        "ALTER TABLE orders ALTER COLUMN status TYPE orderstatus USING status::text::orderstatus")
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'status',
                    existing_type=sa.VARCHAR(),
                    type_=sa.Enum('in_process', 'shipping',
                                  'delivered', name='orderstatus'),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'status',
                    existing_type=sa.Enum(
                        'in_process', 'shipping', 'delivered', name='orderstatus'),
                    type_=sa.VARCHAR(),
                    nullable=True)
    order_status_enum.drop(op.get_bind())
    # ### end Alembic commands ###
