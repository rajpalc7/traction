"""verifier_presentation_requests


Revision ID: 81f17f3e7d8c
Revises: 8ac2e131039d
Create Date: 2022-06-15 00:38:37.999764

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "81f17f3e7d8c"
down_revision = "8ac2e131039d"
branch_labels = None
depends_on = None


create_verifier_presentation_request_timeline_func = """CREATE OR REPLACE FUNCTION verifier_presentation_request_timeline_func() RETURNS trigger AS $body$
    BEGIN
        IF NEW.status IS DISTINCT FROM OLD.status OR NEW.state IS DISTINCT FROM OLD.state THEN
            INSERT INTO "timeline" ( "item_id", "status", "state", "error_status_detail" )
            VALUES(NEW."v_presentation_request_id", NEW."status", NEW."state", NEW."error_status_detail");
            RETURN NEW;
        END IF;
        RETURN null;
    END;
    $body$ LANGUAGE plpgsql
"""  # noqa: E501

drop_verifier_presentation_request_timeline_func = (
    """DROP FUNCTION verifier_presentation_request_timeline_func"""
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "verifier_presentation_request",
        sa.Column(
            "v_presentation_request_id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("tenant_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("contact_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "external_reference_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column("deleted", sa.Boolean(), nullable=False),
        sa.Column("tags", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("comment", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("role", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("state", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "error_status_detail", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column("pres_exch_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column(
            "proof_request", postgresql.JSON(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contact.contact_id"],
        ),
        sa.PrimaryKeyConstraint("v_presentation_request_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("verifier_presentation_request")
    # ### end Alembic commands ###
