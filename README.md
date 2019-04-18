### Quick Start
```python
from wechat_adb_robot.feed_monitor import WeChatFeedMonitor

def push_result(url):
    print("Got new article url", url)

monitor = WeChatFeedMonitor(serial="fe57c975", result_callback=push_result)
monitor.run(skip_first_batch=False)
```
