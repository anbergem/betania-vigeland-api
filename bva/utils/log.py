import logging
import sys


def initialize_logging(*, stdout_level=logging.INFO):
    log = logging.getLogger("bva")
    log.setLevel(logging.DEBUG)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(stdout_level)
    stdout_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    log.addHandler(stdout_handler)