WAR: 基于adb的微信自动化脚本库
===
![python](https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6-blue.svg)
![license](https://img.shields.io/badge/license-MIT%20License-lightgrey.svg)

# What is WAR? & Why WAR?
基于[adb](https://developer.android.com/studio/command-line/adb)的微信自动化脚本库，纯模拟点击项目，支持安卓设备+各种可以使用adb的操作系统（mac, ubuntu已测）。由于业务需要，目前开发主要针对公众号/订阅号的监控/抓取/操作，未来可以加入更多其他脚本，欢迎PR

在使用各种xposed, ipad/mac协议, web协议, 微信hook精疲力竭后，走回了模拟人手的老路。模拟人手永不被封！

# Quick Start
#### 准备工作
1.  usb连接安卓设备，（开发者模式下）启用调试，在设备的开发者模式页勾选允许调试，允许模拟点击。
2.  确保命令[adb](https://developer.android.com/studio/command-line/adb)可用，使用`adb devices`获取`serial`（手机序列号）
    ```shell
    $ adb devices
    List of devices attached
    fe57c975        device
    ```

#### 脚本1: 订阅号监控 `/examples/feed_monitor.py`
1.  安装clipper
    ```
    $ adb -s fe57c975 install apks/clipper1.2.1.apk
    ```
2.  监控订阅号/公众号更新（须已关注），并获取更新的文章列表 
    ```python
    from wechat_adb_robot.scripts.feed_monitor import WeChatFeedMonitor
    from wechat_adb_robot.lib.utils import new_stream_logger

    def push_result(url):
        print("Got new article url, push to db:", url)

    monitor = WeChatFeedMonitor(serial="fe57c975",
                                result_callback=push_result,
                                adb_path="adb",
                                logger=new_stream_logger())
    monitor.run(skip_first_batch=False)  # skip_first_batch=True 可以跳过首次循环的更新识别
    ```
3.  运行结果：
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
    ![example.gif](https://github.com/tommyyz/wechat_adb_robot/raw/master/example.gif)

# Update Info
- 2019.06.27: 增加对6.7.3版本后订阅号页新界面（下图左边屏幕）的支持
  ![compare_v672_v673.jpeg](https://github.com/tommyyz/wechat_adb_robot/raw/master/compare_v672_v673.jpeg)

# TODO List
- [x] 监控订阅号列表更新，并获取更新的文章列表
- [ ] 搜索订阅号并关注
- [ ] 取消关注订阅号
- [ ] 给定列表的公众号历史文章抓取
- [ ] 批量关注好友
- [ ] 自动发朋友圈
- [ ] Tell me: yuhao6066@gmail.com
