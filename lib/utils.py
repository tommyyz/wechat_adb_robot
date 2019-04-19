# coding:utf-8
import logging
import sys


def new_stream_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '[%(asctime)s][%(levelname)s][%(name)s] => %(message)s'))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
