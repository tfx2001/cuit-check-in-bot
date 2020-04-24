from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS
import regex


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "https://bot.stlee.tech"]}})


jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///data.db")}
executors = {"default": ThreadPoolExecutor(1)}
job_defaults = {"coalesce": False, "max_instances": 3}

scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults
)

# scheduler.add_job(print, args=["Hello World"], trigger="interval", seconds=10, id="print")
# print(jobstores["default"].get_all_jobs())

scheduler.start()

from . import views
