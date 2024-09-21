import os
import logging
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler
import pystray
from PIL import Image, ImageDraw


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


# Task tray
def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    return image


logger.info("Task is starting.")

task_icon = pystray.Icon("ItO", create_image(64, 64, 'black', 'white'))
task_icon.run()
