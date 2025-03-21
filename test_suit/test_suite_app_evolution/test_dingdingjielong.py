# -*- coding: utf-8 -*-
"""
Author: chen xi
Date: 2025/2/12 下午5:14
File: test_dingdingjielong.py
"""
import configparser
from datetime import datetime
import time
import pytest
import uiautomator2_extended
from xrs_serial import serial_bitstream
from router_config import modify_wifi, read_config, router_management, get_sections
from adb_commands import AdbManager
from device_reset import reset


@pytest.mark.case_name("接龙")
@pytest.mark.jielong
@pytest.mark.test_environment
@pytest.mark.repeat(1)
# @pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_jielong():
    # 启动app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '钉钉')
    time.sleep(15)
    app.go_to_page('全体群')
    time.sleep(5)
    while not app.exists_element('立即接龙'):
        time.sleep(0.1)
    