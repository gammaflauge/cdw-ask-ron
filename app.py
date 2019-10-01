import datetime
import os
import random

from flask import Flask, render_template
import redcap

from helpers import Table, Workflow

app = Flask(__name__)


RC_TOKEN = os.environ.get("RC_TOKEN")
RC_URI = os.environ.get("RC_URI", "https://redcap.chop.edu/api/")
PROJECT = redcap.Project(RC_URI, RC_TOKEN)


def get_tables(rc_record_id):
    """read in the tables file from redcap, return a json object of the results"""
    table_file, headers = PROJECT.export_file(record=rc_record_id, field="tables")
    tables = table_file.decode(headers["charset"])

    final_tables = []
    for row in tables.strip().split("\n"):
        table_name, table_ts = [r.strip() for r in row.split(",")]
        final_tables.append(Table(table_name, table_ts))

    return final_tables


def get_workflows(rc_record_id):
    workflow_file, headers = PROJECT.export_file(record=rc_record_id, field="workflows")
    workflows = workflow_file.decode(headers["charset"])

    final_workflows = []
    for row in workflows.strip().split("\n"):
        wf_name, wf_status = [r.strip() for r in row.split(",")]
        final_workflows.append(Workflow(wf_name, wf_status))

    return final_workflows


@app.route("/")
def homepage():
    # grab todays record from redcap
    rc_record_id = datetime.date.today().strftime("%Y%m%d")
    data = PROJECT.export_records(records=[rc_record_id])

    if len(data) == 0:
        # no record for today
        return render_template(
            "index.html", error="No record of any activity yet today."
        )
    if len(data) > 1:
        # would not expect more than one record
        return render_template(
            "index.html", error="More than one record in redcap... something is wrong"
        )

    # only one data record, looks ok to proceed
    as_of_datetime = data[0]["as_of_datetime"]
    tables = get_tables(rc_record_id)
    g2g_tables = len([table for table in tables if table.good_to_go])
    total_tables = len(tables)

    workflows = get_workflows(rc_record_id)
    g2g_workflows = len([workflow for workflow in workflows if workflow.good_to_go])
    total_workflows = len(workflows)

    return render_template(
        "index.html",
        as_of=as_of_datetime,
        tables=tables,
        total_tables=total_tables,
        g2g_tables=g2g_tables,
        workflows=workflows,
        total_workflows=total_workflows,
        g2g_workflows=g2g_workflows,
    )


if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)
