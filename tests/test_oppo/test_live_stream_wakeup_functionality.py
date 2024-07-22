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


@pytest.mark.run(order=1)
@pytest.mark.repeat(300)
def test_live_stream_wakeup_functionality(setup_ruiboshi:Uiautomator2SophisticatedExecutor):
    app = setup_ruiboshi
    app.go_to_page("直播", "000547")
    time.sleep(10)
    app.go_to_page("截图")
    app.driver.app_stop(d.appPackage)
    # time.sleep(60 + (i % 20)*30)
    time.sleep(30)
