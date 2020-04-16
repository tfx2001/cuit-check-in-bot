#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
from os import environ

from src import check_in

if __name__ == "__main__":
    shceduler = BlockingScheduler()
    shceduler.add_job(
        check_in.checkIn,
        "cron",
        hour=10,
        minute=00,
        args=[environ["STUDENT_ID"], environ["STUDENT_PASSWORD"]],
    )
    try:
        print(f"学号：{environ['STUDENT_ID']}")
        print("调度器已启动。")
        shceduler.start()
    except KeyboardInterrupt:
        pass
