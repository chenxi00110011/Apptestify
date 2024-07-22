# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
import time
from uiautomator2_extended import Uiautomator2SophisticatedExecutor
import pytest
import ntp_util
from loguru import logger
from config_module import ConfigManagerRUIBOSHI as rui

logger.add(rui.LOGS_DIR + f"\\{ntp_util.timestamp_to_date()}.log", encoding="utf-8")

# delay_list = [60, 120, 300, 600]
users = ["18086409233", "13638601129"]
# sleep_times = range(30)
dids = ['卧室23',
        '家24']
wake_up_times = {'直播唤醒': [],
                 '设置唤醒': []}


@pytest.mark.aov_wakeup_20240628
@pytest.mark.parametrize("did", dids)
def test_pull_live_stream_01(did: str, setup_ruiboshi: Uiautomator2SophisticatedExecutor):
    sleep_time = 30
    logger.info(f"设备休眠时间为{sleep_time}秒")
    time.sleep(sleep_time)
    app = setup_ruiboshi
    app.did = did
    app.go_to_page("首页",'13590267955', 'ljf123456')
    start_time = time.time()
    app.go_to_page("直播", did)
    count = 0
    while not app.exists_element(value="云台"):
        count += 1
        if count >= 30:
            logger.error("直播预览出流超时")
            break
        logger.info("未检测到设备出流")
    end_time = time.time()
    wake_up_time = end_time - start_time
    wake_up_times['直播唤醒'].append(wake_up_time)
    logger.debug("***********************进入直播用时{:.2f}秒**********************".format(wake_up_time))
    wake_up_list = [num for num in wake_up_times['直播唤醒'] if num <= 60]
    logger.debug(wake_up_list)
    logger.debug(sum(wake_up_list)/len(wake_up_list))
    app.title['wakeup_time'] = "{:.2f}".format(wake_up_time)
    time.sleep(10)
    app.go_to_page("截图")
    app.app_stop_()


# @pytest.mark.aov_wakeup_02_oppo
# @pytest.mark.parametrize("sleep_time", sleep_times)
# @pytest.mark.repeat(1)
# def test_pull_live_stream_02(sleep_time: int, setup_ruiboshi: Uiautomator2SophisticatedExecutor):
#     did = '000602'
#     sleep_time = 20.0 - sleep_time/10.0
#     logger.info(f"设备休眠时间为{sleep_time}秒")
#     time.sleep(sleep_time)
#     app = setup_ruiboshi
#     app.did = did
#     start_time = time.time()
#     app.go_to_page("直播", did)
#     count = 0
#     while not app.exists_element(value="云台"):
#         count += 1
#         if count >= 30:
#             logger.error("直播预览出流超时")
#             break
#         logger.info("未检测到设备出流")
#     end_time = time.time()
#     wake_up_time = end_time - start_time
#     wake_up_times['直播唤醒'].append(wake_up_time)
#     logger.debug("***********************进入直播用时{:.2f}秒**********************".format(wake_up_time))
#     wake_up_list = [num for num in wake_up_times['直播唤醒'] if num <= 30]
#     logger.debug(wake_up_list)
#     logger.debug(sum(wake_up_list)/len(wake_up_list))
#     app.title['wakeup_time'] = "{:.2f}".format(wake_up_time)
#     time.sleep(10)
#     app.go_to_page("截图")
#

