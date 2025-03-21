# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
import time
import os
import schedule
import threading

from uiautomator2_extended import Uiautomator2SophisticatedExecutor
from uiautomator2_manager import uiautomator2_extended
import pytest
import xrs_adb
import ntp_util

# delay_list = [60, 120, 300, 600]
users = ["18086409233", "13638601129"]


@pytest.mark.aov_device_binding_success
@pytest.mark.repeat(1000)
def test_aov_device_binding_success(setup_ruiboshi: Uiautomator2SophisticatedExecutor):
    app = setup_ruiboshi
    for user in users:
        if app.exists_element(value="0101"):
            app.go_to_page("删除设备")
        app.go_to_page("扫描二维码")
        time.sleep(10)
        app.go_to_page("截图")
        app.go_to_page("首页")
        app.go_to_page("删除设备")
        app.go_to_page("登录")
        app.go_to_page("首页", user, "cx123456")
        time.sleep(60)
