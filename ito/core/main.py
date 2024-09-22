import os
import sys
import logging
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler
import psutil
import pystray
from PIL import Image


# Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stream_handler = RichHandler(rich_tracebacks=True)
stream_handler.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
logger.addHandler(stream_handler)

log_folder = os.path.join(os.path.dirname(__file__), "../logs")
if not os.path.isdir(log_folder):
    os.mkdir(log_folder)

file_handler = RotatingFileHandler(
    filename=os.path.join(log_folder, "core.log"), encoding="utf-8", maxBytes=1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    "[%(asctime)s] %(levelname)s %(filename)s:%(lineno)d [%(name)s] %(message)s"))
logger.addHandler(file_handler)


# Double active check
pid_file = os.path.join(os.path.dirname(__file__), "../core_pid.txt")

if os.path.exists(pid_file):
    with open(pid_file, "r") as f:
        pid = int(f.read())
    if psutil.pid_exists(pid):
        logger.error(f"Program is already running with PID {pid}.")
        sys.exit(0)

with open(pid_file, "w") as f:
    f.write(str(os.getpid()))


def main(icon: pystray._base.Icon):
    icon.visible = True


# Task tray
icon_file = os.path.join(os.path.dirname(__file__), "../assets/ito.png")
task_icon = pystray.Icon("ito", Image.open(icon_file), "ItO")
task_icon.run(server.main)
