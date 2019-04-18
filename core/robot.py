# coding:utf-8
import logging
import re
import time
from lxml import etree
import os.path as op
import subprocess

logger = logging.getLogger("adb_robot")


class ADBRobot:
    def __init__(self, serial, temp_dump_file='/sdcard/wechat_dump.xml'):
        self.serial = serial
        self.temp_dump_file = temp_dump_file

    def shell(self, cmd=None, decode=True):
        """
        运行指定的cmd命令
        :param cmd:
        :return:
        """
        logger.debug("running shell: {}".format(cmd))
        proc = subprocess.Popen("{} -s {} shell {}".format("adb", self.serial, cmd),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        if decode:
            stdout = stdout.decode()
            stderr = stderr.decode()
        if len(stderr) != 0:
            return stderr
        else:
            return stdout
        return stdout

    def is_app_installed(self, app_name):
        return len(self.shell("pm list packages | grep {}".format(app_name))) > 0

    def run_app(self, app_name):
        """
        app_name = "com.tencent.mm"
        """
        self.shell("monkey -p {} -c android.intent.category.LAUNCHER 1".format(app_name))

    def is_screen_on(self):
        result1 = self.shell('dumpsys input_method | grep mInteractive=true')
        result2 = self.shell('dumpsys input_method | grep mScreenOn=true')
        return result1 != "" or result2 != ""

    def screen_on(self):
        if not self.is_screen_on():
            self.shell('input keyevent 26')

    def screen_off(self):
        if self.is_screen_on():
            self.shell('input keyevent 26')
    
    def go_home(self):
        self.shell('input keyevent 3')

    def go_back(self):
        self.shell('input keyevent 4')

    def enter(self):
        self.shell('input keyevent 66')

    def tap(self, x, y):
        self.shell("input tap {} {}".format(x, y))

    def uidump_and_get_node(self, retry_times=3):
        """
        获得当前页面node
        """
        node = None
        error = None

        for _ in range(retry_times):
            try:
                self.shell("uiautomator dump {}".format(self.temp_dump_file))
                dumps = self.shell("cat {}".format(self.temp_dump_file), decode=False)
                logger.debug(dumps.decode('utf-8'))
                node = etree.XML(dumps)
                break
            except Exception as e:
                logger.exception(e)
                error = e
        
        if node is None:
            raise error
        return node

    def activity_top(self):
        """
        判断当前的应用程序是什么
        """
        return self.shell("dumpsys activity top")

    def get_node_bounds(self, attr_name, attr_value, dumps=None):
        if dumps is None:
            dumps = self.uidump_and_get_node()
        try:
            bounds = dumps.xpath('//node[@{}="{}"]/@bounds'.format(attr_name, attr_value))[0]
        except Exception as e:
            return False
        return bounds
    
    def get_points_in_bounds(self, bounds):
        """
        '[42,1023][126,1080]' => 42, 1023, 126, 1080
        """
        points = re.compile(
            r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]').match(bounds).groups()
        return list(map(int, points))

    def click_bounds(self, bounds):
        """
        bounds = '[42,1023][126,1080]'
        """
        bounds_points = self.get_points_in_bounds(bounds)
        self.tap((bounds_points[0] + bounds_points[2]) / 2,
                 (bounds_points[1] + bounds_points[3]) / 2)

    def ensure_clipboard(self):
        """
        开启clipper软件 https://github.com/majido/clipper
        """
        if not self.is_app_installed("ca.zgrs.clipper"):
            raise ValueError(
                "clipper not installed! please install first: adb install -r apks/clipper1.2.1.apk")
        self.run_app("ca.zgrs.clipper")

    def get_clipboard_text(self):
        """
        确保已安装clipper软件并开启 https://github.com/majido/clipper
        """
        dumps = self.shell("am broadcast -a clipper.get")
        matched = re.compile(r'[\s\S]*data="(.*?)"[\s\S]*').match(dumps)
        if matched:
            text = matched.groups()[0]
        else:
            logger.error(
                "get_clipboard_text error, make sure clipper app is running!")
            text = ""
        return text
