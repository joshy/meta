import json
import logging
import os
import shlex
import subprocess
import sys
from datetime import datetime

import pandas as pd
import requests
import schedule
from flask import Blueprint, current_app, Flask, g, jsonify, render_template, request
from flask_assets import Bundle, Environment

import luigi

# from crawler.config import get_report_show_url
# from crawler.query import query_accession_number
# from tasks.ris_pacs_merge_upload import DailyUpConvertedMerged, MergePacsRis

try:
    import uwsgi

    ex = os.path.join(uwsgi.opt["venv"].decode("latin1"), "bin/python")
except (ImportError, KeyError):
    ex = sys.executable

crawler = Blueprint(
    "crawler",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/crawler/static",
)


"""
assets = Environment(current_app)
js = Bundle(
    "js/jquery-3.3.1.min.js",
    "js/jquery.noty.packaged.min.js",
    "js/script.js",
    filters="jsmin",
    output="gen/packed.js",
)
assets.register("js_all", js)
"""


@crawler.app_template_filter("to_date")
def to_date(date_as_int):
    if date_as_int:
        return datetime.strptime(str(date_as_int), "%Y%m%d").strftime("%d.%m.%Y")
    else:
        return ""


@crawler.route("/")
def main():
    luigi_scheduler = current_app.config["LUIGI_SCHEDULER"]
    return render_template(
        "index.html",
        luigi_scheduler=luigi_scheduler,
        version=current_app.config["VERSION"],
        params={}
    )
