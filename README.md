# WAR: 基于adb的微信自动化脚本库

## What is WAR
基于adb的微信自动化脚本库，纯adb项目，支持各种可以使用adb的操作系统。由于业务需要，主要针对公众号/订阅号的监控/抓取/操作

## Why WAR
在使用各种xposed, ipad/mac协议, web协议, 微信hook战斗无果后，走回了使用自动化脚本的老路。ADB永不被封！

## Quick Start
#### 准备工作
1. usb连接安卓设备，（开发者模式下）启用调试，在设备上点击允许调试。
2. 确保命令[adb](https://developer.android.com/studio/command-line/adb)可用，使用`adb devices`获取`serial`（手机序列号）
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
    import logging, sys
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

    monitor = WeChatFeedMonitor(serial="fe57c975", result_callback=push_result, logger=new_stream_logger())
    monitor.run(skip_first_batch=False)
    ```
3. 运行结果：
    ```
    [14:46:57][INFO][root] => 开始第0次循环
    [14:47:12][INFO][root] => 最新更新的公众号：['金融宽课', '越甲策市', '招商汽车研究', 'IPP评论', '中国教育新闻网', '随手札记', '市川新田三丁目', '中金点睛']
    [14:47:28][INFO][root] => 输出结果：https://mp.weixin.qq.com/s/mPxaA9oGK5X3FNBWb2aeVQ
    [14:47:44][INFO][root] => 输出结果：https://mp.weixin.qq.com/s/YhQtDCRCPnhpplkWA6YtGQ
    [14:48:00][INFO][root] => 输出结果：https://mp.weixin.qq.com/s/Jm16fIMycBs4YT_Wn62apw
    
    ...

    [14:50:58][INFO][root] => 开始第1次循环
    [14:51:14][INFO][root] => 最新更新的公众号：[]
    [14:51:46][INFO][root] => 开始第2次循环
    [14:52:01][INFO][root] => 最新更新的公众号：[]
    [14:52:34][INFO][root] => 开始第3次循环
    
    ...
    ```

## Done List
- 监控订阅号列表更新，并获取更新的文章列表

## Todo List
- 搜索订阅号并关注
- 取消关注订阅号
