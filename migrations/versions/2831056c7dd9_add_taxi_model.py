"""Add taxi model

Revision ID: 2831056c7dd9
Revises: 4934186b5ce0
Create Date: 2015-04-17 17:39:15.767124

"""

# revision identifiers, used by Alembic.
revision = '2831056c7dd9'
down_revision = '4934186b5ce0'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('taxi',
    sa.Column('added_at', sa.DateTime(), nullable=True),
    sa.Column('added_via', sa.Enum('form', 'api', name='sources_taxi'), nullable=False),
    sa.Column('source', sa.String(length=255), nullable=False),
    sa.Column('last_update_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vehicle_id', sa.Integer(), nullable=True),
    sa.Column('ads_id', sa.Integer(), nullable=True),
    sa.Column('conducteur_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('free', 'occupied', 'oncoming', 'off', name='status_taxi_enum'), nullable=True),
    sa.Column('added_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['added_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['ads_id'], ['ADS.id'], ),
    sa.ForeignKeyConstraint(['conducteur_id'], ['conducteur.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicle.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('taxi')
    ### end Alembic commands ###
