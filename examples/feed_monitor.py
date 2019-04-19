# coding:utf-8
import logging
import sys
from wechat_adb_robot.scripts.feed_monitor import WeChatFeedMonitor


def push_result(url):
    print("Got new article url:", url)


def new_stream_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '[%(asctime)s][%(levelname)s][%(name)s] => %(message)s'))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


if __name__ == "__main__":
    # Assume we already have device[serial=fe57c975] attached and has clipper installed
    monitor = WeChatFeedMonitor(
        serial="fe57c975", result_callback=push_result, logger=new_stream_logger())
    monitor.run(skip_first_batch=False)
