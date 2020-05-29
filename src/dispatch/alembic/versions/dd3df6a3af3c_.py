"""Generalizes data model for incident reports (tactical, executive)

Revision ID: dd3df6a3af3c
Revises: a57934336710
Create Date: 2020-05-21 15:33:15.592184

"""
from alembic import op

import sqlalchemy as sa
import sqlalchemy_utils

from dispatch.report.enums import ReportTypes
from dispatch.report import service as report_service

# revision identifiers, used by Alembic.
revision = "dd3df6a3af3c"
down_revision = "a57934336710"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    reports = bind.execute("select id, conditions, actions, needs from status_report")

    op.rename_table("status_report", "report")
    op.add_column(
        "report", sa.Column("details", sqlalchemy_utils.types.json.JSONType(), nullable=True)
    )
    op.add_column("report", sa.Column("details_raw", sa.String(), nullable=True))
    op.add_column(
        "report",
        sa.Column("search_vector", sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True),
    )
    op.add_column(
        "report",
        sa.Column("type", sa.String(), server_default=ReportTypes.tactical_report, nullable=False),
    )
    op.add_column("document", sa.Column("report_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "document", "report", ["report_id"], ["id"])
    op.create_index(
        "ix_report_search_vector", "report", ["search_vector"], unique=False, postgresql_using="gin"
    )

    for id, conditions, actions, needs in reports:
        report = report_service.get(db_session=session, report_id=id)
        report.details = {"conditions": conditions, "actions": actions, "needs": needs}
        report.details_raw = f"Conditions: {conditions}; Actions: {actions}; Needs: {needs}"
        session.add(report)
        session.commit()

    op.drop_column("report", "conditions")
    op.drop_column("report", "actions")
    op.drop_column("report", "needs")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_report_search_vector", table_name="report")
    op.drop_column("report", "search_vector")
    op.rename_table("report", "status_report")
    op.add_column(
        "status_report", sa.Column("conditions", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "status_report", sa.Column("actions", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "status_report", sa.Column("needs", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###