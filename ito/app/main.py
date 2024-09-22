import os
import logging
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler
import flet as ft


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
    filename=os.path.join(log_folder, "app.log"), encoding="utf-8", maxBytes=1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    "[%(asctime)s] %(levelname)s %(filename)s:%(lineno)d [%(name)s] %(message)s"))
logger.addHandler(file_handler)


# Main
def main(page: ft.Page):
    t = ft.Text(value="Hello, world!", color="green")
    page.controls.append(t)
    page.update()


ft.app(main)
