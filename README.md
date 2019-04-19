# WAR: 基于adb的微信自动化脚本库

## What is WAR
基于adb的微信自动化脚本库，纯adb项目，支持各种可以使用adb的操作系统。由于业务需要，主要针对公众号/订阅号的监控/抓取/操作

## Why WAR
在使用各种xposed, ipad/mac协议, web协议, 微信hook战斗无果后，走回了使用自动化脚本的老路。ADB永不被封！

## Quick Start
#### 准备工作
确保命令`adb`可用，使用`adb devices`获取`serial`（手机序列号）：
```shell
$ adb devices
List of devices attached
fe57c975        device
```

#### 订阅号监控
1. 安装clipper
    ```
    $ adb -s fe57c975 install apks/clipper1.2.1.apk
    ```
2. 监控订阅号/公众号更新，并获取更新的文章列表
    ```python
    from wechat_adb_robot.feed_monitor import WeChatFeedMonitor

    def push_result(url):
        print("Got new article url", url)

    monitor = WeChatFeedMonitor(serial="fe57c975", result_callback=push_result)
    monitor.run(skip_first_batch=False)
    ```


## Done List
- 监控订阅号列表更新，并获取更新的文章列表

## Todo List
- 搜索订阅号并关注
- 取消关注订阅号
