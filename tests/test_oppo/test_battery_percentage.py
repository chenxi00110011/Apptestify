# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
import re
import time
from uiautomator2_extended import Uiautomator2SophisticatedExecutor
import pytest
import ntp_util
from loguru import logger
from config_module import ConfigManagerRUIBOSHI as rui
from xrs_serial import serial_bitstream

logger.add(rui.LOGS_DIR + f"\\{ntp_util.timestamp_to_date()}.log", encoding="utf-8")

com = 'com38'
battery_level = 10


@pytest.mark.battery_percentage
@pytest.mark.flaky(reruns=3, reruns_delay=10)
def test_pull_live_stream(setup_ruiboshi: Uiautomator2SophisticatedExecutor):
    app = setup_ruiboshi
    time.sleep(10)
    app.go_to_page('设备设置', '000507')
    app.go_to_page('获取电量')
    print(app.title)
    match = re.search(r'\d+', app.title['text'])
    battery_percentage = None
    if match:
        battery_percentage = int(match.group())
        print("电池电量:", battery_percentage, "%")
    else:
        raise Exception("未找到电池电量信息")
    if battery_percentage is not None and battery_percentage <= battery_level:
        serial_bitstream(com, '上电', 1)
    else:
        serial_bitstream(com, '断电', 1)
    app.app_stop_()
