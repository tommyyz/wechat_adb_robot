# coding:utf-8
import logging
import re
import time
from wechat_adb_robot.core.robot import ADBRobot


class FeedItem():
    def __init__(self, node):
        self.node = node
        self.account_name = node.xpath(
            'node[@index="0"]/node[@index="0"]/node[@index="0"]/@text')[0]
        self.last_article_time = node.xpath(
            'node[@index="0"]/node[@index="1"]/@text')[0]
        self.last_article_title = node.xpath(
            'node[@index="1"]/node[@index="0"]/node[@index="0"]/@text')[0]
        self.bounds = node.xpath('@bounds')[0]


class FeedArticleItem():
    def __init__(self, node):
        self.node = node
        self.bounds = node.xpath('@bounds')[0]


class WeChatFeedMonitor():
    def __init__(self, serial, result_callback=lambda x: x, adb_path='adb', logger=None):
        self.bot = ADBRobot(serial, adb_path=adb_path)
        self.result_callback = result_callback
        self.last_feed_list = []
        self.logger = logger if logger else logging.getLogger("feed_monitor")
    
    def run(self, skip_first_batch=True, sleep_interval=30):
        """
        循环执行脚本
        由于微信的一些机制，盯着订阅号页不动是不会有更新的，所以本脚本会熄屏开屏以模仿人的操作，试下来感觉良好
        :param skip_first_batch: 是否保存并跳过第一次截取的最新订阅列表
        :param sleep_interval: 熄屏时间
        """
        loop_index = 0
        while True:
            self.logger.info("开始第{}次循环".format(loop_index))
            # 亮屏
            self.bot.screen_on()

            # 打开剪贴板app
            self.bot.ensure_clipboard()

            # 返回桌面
            self.bot.go_home()
            time.sleep(1)

            # 打开微信首页
            self.ensure_wechat_front()
            time.sleep(1)

            # 进入订阅号页
            self.go_feed_page()
            time.sleep(2)

            if skip_first_batch and loop_index == 0:
                # 保存并跳过第一次截取的最新订阅列表
                self.get_feed_list_and_find_updates(set_new=True)
            else:
                # 执行订阅列表监听
                self.feed_monitoring()

            # 返回微信首页
            self.bot.go_back()

            # 返回桌面
            self.bot.force_home()
            time.sleep(1)

            # 熄屏
            self.bot.screen_off()

            loop_index += 1
            time.sleep(sleep_interval)
    
    def ensure_wechat_front(self):
        """
        保证微信在前台，并在首页
        """
        self.bot.run_app("com.tencent.mm")
        for _ in range(6):
            # 可能不在首页，按返回键6次基本可以确定重新打开为首页
            # TODO: 使用uidump检查是否在微信首页
            self.bot.go_back()
        self.bot.run_app("com.tencent.mm")

    def go_feed_page(self):
        """
        进入订阅号列表页
        """
        # TODO: 增加如果当屏找不到，滚屏继续找的逻辑
        
        dumps = self.bot.uidump_and_get_node()
        bounds672 = self.bot.get_node_bounds("text", "订阅号", dumps=dumps)  # 6.7.3以前版本
        bounds673 = self.bot.get_node_bounds("text", "订阅号消息", dumps=dumps)  # 6.7.3以后版本

        if bounds672:
            self.bot.click_bounds(bounds672)
        elif bounds673:
            self.bot.click_bounds(bounds673)
            time.sleep(2)
            # 如果是6.7.3以后版本，还需点击右上角三条杠更多按钮，进入列表页
            boundsMore = self.bot.get_node_bounds("content-desc", "订阅号")  # 6.7.3以前版本
            if boundsMore:
                self.bot.click_bounds(boundsMore)
            else:
                self.logger.error("找不到订阅号消息页右上角的更多按钮")
        else:
            self.logger.error("找不到订阅号栏，请确认订阅号栏在微信首页")
    
    def get_more_button_on_673_feed_page(self):
        """
        获得订阅号列表页内的第一屏订阅号列表
        """
        page_node = self.bot.uidump_and_get_node()
        return page_node.xpath(
            '//node[@class="android.widget.ListView"]/node/node[@index="1"]')

    def get_feed_list(self):
        """
        获得订阅号列表页内的第一屏订阅号列表
        """
        page_node = self.bot.uidump_and_get_node()
        return [FeedItem(node) for node in page_node.xpath(
            '//node[@class="android.widget.ListView"]/node/node[@index="1"]')]

    def get_feed_list_and_find_updates(self, set_new=True):
        """
        获得订阅号列表页内的第一屏订阅号列表，并找出更新的订阅号条目
        """
        new_feed_list = self.get_feed_list()
        old_account_names = [_.account_name for _ in self.last_feed_list]
        result = []

        for new_feed_item in new_feed_list:
            if new_feed_item.account_name not in old_account_names:
                result.append(new_feed_item)
        
        if set_new:
            self.last_feed_list = new_feed_list

        return result
    
    def get_feed_articles_in_account_page(self):
        """
        获得订阅号详情页内的最新文章列表，通常会在底部
        """
        page_node = self.bot.uidump_and_get_node()
        content_boxes = page_node.xpath(
            '//node[@class="android.widget.FrameLayout"]/node[@class="android.widget.FrameLayout"]/node[@class="android.widget.ListView"]/node[@class="android.widget.RelativeLayout"]/node[@class="android.widget.LinearLayout"]/node[@class="android.widget.LinearLayout"]')
        if len(content_boxes) == 0:
            return []
        last_content_box = content_boxes[len(content_boxes) - 1]
        return [FeedArticleItem(node) for node in last_content_box.xpath('node')]
    
    def feed_monitoring(self):
        """
        监控订阅号列表，找出更新的订阅号，进入订阅号并依次点击最新链接，复制到剪贴板输出
        """
        # 获取最近更新的订阅号名单
        newly_update_feed_list = self.get_feed_list_and_find_updates(set_new=True)
        self.logger.info("最新更新的公众号：{}".format(
            [_.account_name for _ in newly_update_feed_list]))
        
        for feed_item in newly_update_feed_list:
            # 进入订阅号详情页
            self.logger.info("进入订阅号[{}]详情页 ...".format(feed_item.account_name))
            self.bot.click_bounds(feed_item.bounds)

            # 获得订阅号的最新文章列表
            feed_articles = self.get_feed_articles_in_account_page()
            self.logger.info("订阅号的最新文章列表的文章个数: {}".format(len(feed_articles)))

            # 查找订阅号的最新文章列表
            for feed_article_item in feed_articles:

                # 点击文章详情页
                self.logger.debug("进入文章详情页 ...")
                self.bot.click_bounds(feed_article_item.bounds)
                time.sleep(2)
                
                # 点击更多
                self.logger.debug("点击更多 ...")
                more_button_bounds = self.bot.get_node_bounds("content-desc", "更多")
                if more_button_bounds:
                    self.bot.click_bounds(more_button_bounds)
                    time.sleep(2)
                else:
                    self.logger.error("找不到更多按钮，文章有问题？")

                # 点击复制链接
                self.logger.debug("点击复制链接 ...")
                copy_link_btn_bounds = self.bot.get_node_bounds("text", "复制链接")
                if copy_link_btn_bounds:
                    self.bot.click_bounds(copy_link_btn_bounds)
                    time.sleep(1)

                    # 获取剪贴板并输出
                    self.output_result(self.bot.get_clipboard_text())
                else:
                    self.logger.error("找不到复制链接按钮，文章有问题？")

                self.logger.debug("返回订阅号页 ...")
                self.bot.go_back()
            self.bot.go_back()

    def output_result(self, url):
        self.logger.info("输出结果：{}".format(url))
        self.result_callback(url)
