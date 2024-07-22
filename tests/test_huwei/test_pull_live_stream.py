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
sleep_times = [60]


@pytest.mark.aov_pull_live_stream
@pytest.mark.parametrize("sleep_time", sleep_times)
@pytest.mark.repeat(1000)
def test_pull_live_stream(sleep_time: int, setup_ruiboshi: Uiautomator2SophisticatedExecutor):
    print(f"设备休眠时间为{sleep_time}秒")
    time.sleep(sleep_time)
    app = setup_ruiboshi
    start_time = time.time()
    app.go_to_page("直播")
    count = 0
    while not app.exists_element(value="云台"):
        count += 1
        if count >= 30:
            print("直播预览出流超时")
            break
        print("未检测到设备出流")
    end_time = time.time()
    print("***********************{:.2f}**********************".format(end_time - start_time))
    app.go_to_page("截图")
