"""new map_id column for routes, cities and connections tables

Revision ID: 1ea31598181b
Revises: a605b394c736
Create Date: 2025-01-27 02:49:35.759324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1ea31598181b'
down_revision: Union[str, None] = 'a605b394c736'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create new 'cities' table
    op.create_table(
        'cities',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('map_id', sa.Integer(), nullable=True),  # Initially nullable
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('position_x', sa.Integer(), nullable=True),
        sa.Column('position_y', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['map_id'], ['maps.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Add 'map_id' column to 'connections' table
    op.add_column('connections', sa.Column('map_id', sa.Integer(), nullable=True))  # Initially nullable
    op.alter_column('connections', 'parent_city_id', existing_type=sa.INTEGER(), nullable=True)
    op.alter_column('connections', 'child_city_id', existing_type=sa.INTEGER(), nullable=True)

    # Migrate existing 'city' data to 'cities'
    conn = op.get_bind()
    conn.execute(sa.text(""" 
        INSERT INTO cities (name, position_x, position_y, map_id)
        SELECT name, position_x, position_y, 1  -- Assuming map_id = 1 (default map) for existing data
        FROM city
    """))

    conn.execute(sa.text(""" 
    UPDATE connections
    SET parent_city_id = (SELECT cities.id FROM cities WHERE cities.name = (SELECT city.name FROM city WHERE city.id = connections.parent_city_id)),
    child_city_id = (SELECT cities.id FROM cities WHERE cities.name = (SELECT city.name FROM city WHERE city.id = connections.child_city_id));
    """))

    # Update foreign key constraints for 'connections'
    op.drop_constraint('connections_parent_city_id_fkey', 'connections', type_='foreignkey')
    op.drop_constraint('connections_child_city_id_fkey', 'connections', type_='foreignkey')
    op.drop_table('city')

    op.create_foreign_key('connections_child_city_id_fkey', 'connections', 'cities', ['child_city_id'], ['id'])
    op.create_foreign_key('connections_parent_city_id_fkey', 'connections', 'cities', ['parent_city_id'], ['id'])
    op.create_foreign_key('connections_map_id_fkey', 'connections', 'maps', ['map_id'], ['id'])

    # Update existing 'connections' entries with map_id = 1
    conn.execute(sa.text("UPDATE connections SET map_id = 1"))

    # Modify 'maps' table columns to allow NULL
    op.alter_column('maps', 'name', existing_type=sa.VARCHAR(length=255), nullable=True)
    op.alter_column('maps', 'size_x', existing_type=sa.INTEGER(), nullable=True)
    op.alter_column('maps', 'size_y', existing_type=sa.INTEGER(), nullable=True)

    # Add 'map_id' column to 'routes' table
    op.add_column('routes', sa.Column('map_id', sa.Integer(), nullable=True))  # Initially nullable
    op.create_foreign_key('routes_map_id_fkey', 'routes', 'maps', ['map_id'], ['id'])

    # Set default map_id = 1 for existing 'routes'
    conn.execute(sa.text("UPDATE routes SET map_id = 1"))

    # Modify 'routes' table columns to allow NULL
    op.alter_column('routes', 'startpoint', existing_type=sa.VARCHAR(length=255), nullable=True)
    op.alter_column('routes', 'endpoint', existing_type=sa.VARCHAR(length=255), nullable=True)
    op.alter_column('routes', 'created_at', existing_type=postgresql.TIMESTAMP(), nullable=True)
    op.alter_column('routes', 'route', existing_type=postgresql.JSON(astext_type=sa.Text()), nullable=True)

    # Now set the 'map_id' columns to NOT NULL
    op.alter_column('routes', 'map_id', nullable=False)
    op.alter_column('cities', 'map_id', nullable=False)
    op.alter_column('connections', 'map_id', nullable=False)


def downgrade() -> None:
    # Recreate 'city' table
    op.create_table(
        'city',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('position_x', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('position_y', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('id', name='city_pkey')
    )

    # Migrate 'cities' data back to 'city'
    conn = op.get_bind()
    conn.execute(sa.text(""" 
        INSERT INTO city (id, name, position_x, position_y)
        SELECT id, name, position_x, position_y
        FROM cities
    """))

    # Remove 'map_id' foreign key constraints and column
    op.drop_constraint('routes_map_id_fkey', 'routes', type_='foreignkey')
    op.drop_column('routes', 'map_id')

    op.drop_constraint('connections_map_id_fkey', 'connections', type_='foreignkey')
    op.drop_constraint('connections_parent_city_id_fkey', 'connections', type_='foreignkey')
    op.drop_constraint('connections_child_city_id_fkey', 'connections', type_='foreignkey')
    op.create_foreign_key('connections_child_city_id_fkey', 'connections', 'city', ['child_city_id'], ['id'])
    op.create_foreign_key('connections_parent_city_id_fkey', 'connections', 'city', ['parent_city_id'], ['id'])

    op.alter_column('connections', 'child_city_id', existing_type=sa.INTEGER(), nullable=False)
    op.alter_column('connections', 'parent_city_id', existing_type=sa.INTEGER(), nullable=False)
    op.drop_column('connections', 'map_id')

    # Drop 'cities' table
    op.drop_table('cities')

    # Revert 'maps' table columns to NOT NULL
    op.alter_column('maps', 'size_y', existing_type=sa.INTEGER(), nullable=False)
    op.alter_column('maps', 'size_x', existing_type=sa.INTEGER(), nullable=False)
    op.alter_column('maps', 'name', existing_type=sa.VARCHAR(length=255), nullable=False)

    # Revert 'routes' table columns to NOT NULL
    op.alter_column('routes', 'route', existing_type=postgresql.JSON(astext_type=sa.Text()), nullable=False)
    op.alter_column('routes', 'created_at', existing_type=postgresql.TIMESTAMP(), nullable=False)
    op.alter_column('routes', 'endpoint', existing_type=sa.VARCHAR(length=255), nullable=False)
    op.alter_column('routes', 'startpoint', existing_type=sa.VARCHAR(length=255), nullable=False)
