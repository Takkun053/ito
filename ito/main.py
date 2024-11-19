import os
import sys
import logging
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler
import psutil
import flet as ft

import app


# Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stream_handler = RichHandler(rich_tracebacks=True)
stream_handler.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
logger.addHandler(stream_handler)

log_folder = os.path.join(os.path.dirname(__file__), "logs")
if not os.path.isdir(log_folder):
    os.mkdir(log_folder)

file_handler = RotatingFileHandler(
    filename=os.path.join(log_folder, "ito.log"), encoding="utf-8", maxBytes=1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    "[%(asctime)s] %(levelname)s %(filename)s:%(lineno)d [%(name)s] %(message)s"))
logger.addHandler(file_handler)


# Double active check
lock_file = os.path.join(os.path.dirname(__file__), "ito.lock")

if os.path.exists(lock_file):
    with open(lock_file) as f:
        lock_data = f.read().split("\n")
        pid = int(lock_data[0])

    if psutil.pid_exists(pid) and str(psutil.Process(pid).create_time()) == lock_data[1]:
        logger.error(f"Program is already running with PID {pid}.")
        ft.app(app.show_alert)
        sys.exit()
    else:
        os.remove(lock_file)

with open(lock_file, "w") as f:
    f.write(str(os.getpid()) + "\n" +
            str(psutil.Process(os.getpid()).create_time()))


# Main
ft.app(app.main)
