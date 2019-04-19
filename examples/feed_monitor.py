# coding:utf-8
from wechat_adb_robot.scripts.feed_monitor import WeChatFeedMonitor
from wechat_adb_robot.lib.utils import new_stream_logger


def push_result(url):
    print("Got new article url:", url)


if __name__ == "__main__":
    # Assume we already have device[serial=fe57c975] attached and has clipper installed
    monitor = WeChatFeedMonitor(serial="fe57c975",
                                result_callback=push_result,
                                adb_path="adb",
                                logger=new_stream_logger())
    monitor.run(skip_first_batch=False)
