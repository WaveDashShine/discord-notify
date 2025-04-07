import logging
from configs import ROOT_PATH
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s: "
    "%(filename)s - %(funcName)s - line:%(lineno)d - %(message)s"
)

file_handler = logging.FileHandler(
    filename=os.path.join(ROOT_PATH, "debug/debug.log"), encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
