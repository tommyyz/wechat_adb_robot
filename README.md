# WAR: 基于adb的微信自动化脚本库

### What is WAR
基于adb的微信自动化脚本库，纯adb项目，支持各种可以使用adb的操作系统。由于业务需要，主要针对微信公众号/订阅号的监控/抓取/操作

### Why WAR
在使用各种xposed, ipad/mac协议, web协议, 微信hook战斗无果后，走回了使用自动化脚本的老路。ADB永不被封！

### Quick Start
监控微信订阅号/公众号更新（须已关注目标），并获取更新的文章列表
```python
from wechat_adb_robot.feed_monitor import WeChatFeedMonitor

def push_result(url):
    print("Got new article url", url)

monitor = WeChatFeedMonitor(serial="fe57c975", result_callback=push_result)
monitor.run(skip_first_batch=False)
```

### Done List
- 监控订阅号列表更新，并获取更新的文章列表

### Todo List
- 搜索订阅号并关注
- 取消关注订阅号
- 批量添加好友
