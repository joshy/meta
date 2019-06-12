import json
import logging
import os
import shlex
import subprocess
import sys
from datetime import datetime

import pandas as pd
import requests
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


assets = Environment(current_app)
js = Bundle(
    "js/jquery-3.3.1.min.js",
    "js/jquery.noty.packaged.min.js",
    "js/script.js",
    filters="jsmin",
    output="gen/packed.js",
)
assets.register("js_all", js)


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
        params={},
    )


@crawler.route("/search")
def search():
    accession_number = request.args.get("accession_number", "")
    day = request.args.get("day", "")
    if not any([accession_number, day]):
        return "no accession number or day given", 400
    w = luigi.worker.Worker(no_install_shutdown_handler=True)
    if accession_number:
        task = MergePacsRis({"acc": accession_number})
    elif day:
        task = MergePacsRis({"day": day})
    w.add(task)
    w.run()
    if task.complete():
        with task.output().open("r") as r:
            results = json.load(r)
            for result in results:
                result["_childDocuments_"] = sorted(
                    result["_childDocuments_"],
                    key=lambda k: int(k["SeriesNumber"] or "0"),
                )

        return render_template(
            "result.html",
            accession_number=accession_number,
            day=day,
            luigi_scheduler=luigi_scheduler,
            version=app.config["VERSION"],
            results=results,
        )
    else:
        return render_template(
            "error.html",
            accession_number=accession_number,
            day=day,
            luigi_scheduler=luigi_scheduler,
            version=app.config["VERSION"],
            results={},
        )


@crawler.route("/upload", methods=["POST"])
def upload():
    data = request.get_json(force=True)
    accession_number = data.get("acc", "")
    day = data.get("day", "")
    logging.debug("Accession number to upload is: {}".format(accession_number))
    if not any([accession_number, day]):
        return "no accession number or day given", 400

    w = luigi.worker.Worker(no_install_shutdown_handler=True)
    if accession_number:
        task = DailyUpConvertedMerged({"acc": accession_number})
    else:
        print("day")
        task = DailyUpConvertedMerged({"day": day})
    w.add(task)
    w.run()
    headers = {"content-type": "application/json"}
    if task.complete():
        return json.dumps({"status": "ok"})
    else:
        return "Task error", 400


@crawler.route("/batch-upload")
def batch():
    from_date = request.args.get("from-date", "")
    to_date = request.args.get("to-date", "")
    accession_number = request.args.get("accession_number")

    if accession_number:
        cmd = (
            ex
            + ' -m tasks.ris_pacs_merge_upload DailyUpConvertedMerged --query \'{"acc": "%s"}\''
            % accession_number
        )
        logging.debug("Running command :", cmd)
        cmds = shlex.split(cmd)
        subprocess.run(cmds, shell=False, check=False)
        return json.dumps({"status": "ok"})
    else:
        if not (any([from_date, to_date])):
            return "From date or to date is missing", 400

        from_date_as_date = datetime.strptime(from_date, "%d.%m.%Y")
        to_date_as_date = datetime.strptime(to_date, "%d.%m.%Y")
        range = pd.date_range(from_date_as_date, to_date_as_date)
        for day in range:
            cur_day = day.strftime("%d.%m.%Y")
            cmd = (
                ex
                + ' -m tasks.ris_pacs_merge_upload DailyUpConvertedMerged --query \'{"day": "%s"}\''
                % cur_day
            )

            logging.debug("Running command :", cmd)
            cmds = shlex.split(cmd)
            subprocess.run(cmds, shell=False, check=False)
        return json.dumps({"status": "ok"})
