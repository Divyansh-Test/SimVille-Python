import logging

logging.basicConfig(
    filename="app.log",
    filemode="w",   # overwrite file on each run
    level=logging.INFO,
    format="%(asctime)s | %(filename)s | %(message)s"
)
logger=logging.getLogger(__name__)
def get_logger(name):
    return logging.getLogger(name)
