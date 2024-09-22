import os
import sys
import logging
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler
import psutil
import pystray
from PIL import Image

import server


PRODUCT = getattr(sys, "frozen", False)


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
lock_file = os.path.join(os.path.dirname(__file__), "../core.lock")

if os.path.exists(lock_file):
    with open(lock_file) as f:
        lock_data = f.read().split("\n")
        pid = int(lock_data[0])

    if psutil.pid_exists(pid) and str(psutil.Process(pid).create_time()) == lock_data[1]:
        logger.error(f"Program is already running with PID {pid}.")
        sys.exit()
    else:
        os.remove(lock_file)

with open(lock_file, "w") as f:
    f.write(str(os.getpid()) + "\n" +
            str(psutil.Process(os.getpid()).create_time()))


# Arg check
if len(sys.argv) <= 1:
    logger.error("Insufficient number of arguments.")
    sys.exit()


# Main
def main(icon: pystray._base.Icon):
    icon.visible = True
    match sys.argv[1]:
        case "run":
            server.main(icon)


# Task tray
icon_file = os.path.join(os.path.dirname(
    __file__), "assets/ito.png" if PRODUCT else "../assets/ito.png")
task_icon = pystray.Icon("ito", Image.open(icon_file), "ItO")
task_icon.run(main)
