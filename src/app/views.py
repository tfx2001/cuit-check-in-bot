from flask import request, jsonify
import apscheduler

from . import app, scheduler
from .utils import checkIn, login


@app.route("/add", methods=["POST"])
def index():
    jsonData = request.json
    loginRet = login(jsonData["studentID"], jsonData["password"])
    if loginRet != 0:
        return jsonify({"code": -1, "msg": loginRet})
    else:
        try:
            scheduler.add_job(
                checkIn,
                args=[jsonData["studentID"], jsonData["password"]],
                trigger="cron",
                hour="7",
                id=jsonData["studentID"],
                misfire_grace_time=3600
            )
            return jsonify({"code": 0})
        except apscheduler.jobstores.base.ConflictingIdError:
            return jsonify({"code": -2, "msg": "请勿重复提交！"})


@app.route("/delete", methods=["POST"])
def delete():
    jsonData = request.json
    loginRet = login(jsonData["studentID"], jsonData["password"]);
    if loginRet != 0:
        return jsonify({"code": -1, "msg": loginRet})
    else:
        try:
            scheduler.remove_job(jsonData["studentID"])
            return jsonify({"code": 0})
        except  apscheduler.schedulers.base.JobLookupError:
            return jsonify({"code": -2, "msg": "账号未登记！"})


@app.route("/ping")
def ping():
    return "pong"
