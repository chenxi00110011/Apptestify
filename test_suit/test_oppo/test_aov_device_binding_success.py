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

# delay_list = [60, 120, 300, 600]
users = ["18086409233", "13638601129"]
time_sleep = 60


@pytest.mark.aov_device_binding_success
@pytest.mark.timeout(300)
def test_aov_device_binding_success(setup_ruiboshi: Uiautomator2SophisticatedExecutor):
    time.sleep(time_sleep)
    app = setup_ruiboshi
    for user in users:
        app.go_to_page("首页", user, "cx123456")
        if app.exists_element(value="000602"):
            app.go_to_page("删除设备")
        start_time = time.time()
        app.go_to_page("扫描二维码")
        end_time = time.time()
        time.sleep(10)
        app.title['wakeup_time'] = '{:.2f}'.format(end_time-start_time)
        app.go_to_page("截图")
        app.go_to_page("首页")
        app.go_to_page("删除设备")
        app.go_to_page("登录")

