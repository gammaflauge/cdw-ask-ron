import datetime
import os
import random

from flask import Flask
import redcap


app = Flask(__name__)


RC_TOKEN = os.environ.get("RC_TOKEN", "FCAF1AF9553EEF4F9E34FEA60A7EC8DF")
RC_URI = os.environ.get("RC_URI", "https://redcap.chop.edu/api/")
PROJECT = redcap.Project(RC_URI, RC_TOKEN)

CHECKMARK = "&#9989;"
RED_X = "&#10060;"


@app.route("/")
def homepage():
    # grab todays record from redcap
    rc_record_id = datetime.date.today().strftime("%Y%m%d")
    data = PROJECT.export_records(records=[rc_record_id])

    # process tables
    table_file, headers = PROJECT.export_file(record=rc_record_id, field="tables")
    tables = table_file.decode(headers["charset"])
    compare_date_str = datetime.date.today().strftime("%Y-%m-%d 00:00:00")

    table_html = """<h3>Tables</h3>"""
    for row in tables.strip().split("\n"):
        table_name, table_ts = [r.strip() for r in row.split(",")]
        emoji = CHECKMARK
        if table_ts < compare_date_str:
            # table was not updated today
            emoji = RED_X
        table_html += f"""<p>{ emoji } { table_name } ({ table_ts })</p>"""

    # process workflows
    workflow_file, headers = PROJECT.export_file(record=rc_record_id, field="workflows")
    workflows = workflow_file.decode(headers["charset"])

    wf_html = """<h3>Workflows</h3>"""
    for row in workflows.strip().split("\n"):
        emoji = CHECKMARK
        wf_name, wf_status = [r.strip() for r in row.split(",")]
        if wf_status.strip() != "True":
            emoji = RED_X
        wf_html += f"""<p>{ emoji } { wf_name }</p>"""

    return f"""
    <h1>CDW Status as of { data[0]["as_of_datetime"] }</h1>
    { table_html }
    { wf_html }
    """


if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)
