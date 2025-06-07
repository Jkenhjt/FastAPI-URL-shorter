"""create test table

Revision ID: 3fcb07993118
Revises:
Create Date: 2025-06-07 19:34:21.538894

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3fcb07993118"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("alembic_test_table", sa.Column("alembic_name", sa.String()))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("alembic_test_table")
    pass
