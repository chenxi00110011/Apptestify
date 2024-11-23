# 分享设备
import time
import os.path
import time
import pytest

import ntp_util
import uiautomator2_extended
from adb_commands import AdbManager
from config_module import get_config
from router_config import read_config
from image_popup import show_image
import threading
from device_reset import reset

import uiautomator2_extended
account_config = read_config(r'..\..\config\base.ini')
app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
time.sleep(15)
app.run_parameters['rectangle'] = 1.0
app.go_to_page("登录")
app.go_to_page('首页', account_config.get('睿博士测试手机账号', 'account'),
               account_config.get('睿博士测试手机账号', 'pwd'))
app.go_to_page('二维码', '007004', '分享管理')

# 截图
bounds = app.driver(resourceId="com.zwcode.p6slite:id/qr_iv").info["bounds"]
app.save_screenshotV1(bounds)