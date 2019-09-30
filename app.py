import os
import random

from flask import Flask
import redcap


app = Flask(__name__)


RC_TOKEN = os.environ.get("RC_TOKEN")
RC_URI = os.environ.get("RC_URI")
PROJECT = redcap.Project(RC_URI, RC_TOKEN)


@app.route("/")
def homepage():
    data = PROJECT.export_records()
    rec = random.choice(data)

    return f"""
    <h1>{ rec["mantra"] }</h1>
    <p style="font-size:100px">&#129409;</p>"""


if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)
