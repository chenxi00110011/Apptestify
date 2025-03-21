# -*- coding: utf-8 -*-
"""
Author: chen xi
Date: 2025/1/14 上午9:18
File: test_aov_wakeup.py
"""
import time
import pytest
import uiautomator2_extended
from datetime import datetime

from xrs_serial import serial_bitstream

# 计数唤醒失败次数
wakeFailCount = 0
parameter = [
    '005995',
    '011364',
    '011380'
]


@pytest.mark.aov
@pytest.mark.case_name("设备唤醒")
@pytest.mark.parametrize("name", parameter)
@pytest.mark.repeat(5)
def test_aov_wakeup(name):
    global wakeFailCount
    # 启动APP
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(20)
    app.go_to_page("首页", '18086409233', 'cx123456')
    app.WAIT_TIME = 0
    app.go_to_page('直播', name)
    start_time = time.time()
    count = 0
    while not app.exists_element(selector="text", value="画质") and count < 30:
        count += 1
        time.sleep(0.5)
    end_time = time.time()

    # 获取当前时间并格式化为字符串
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 要写入的内容
    content = "{:.2f}".format(end_time - start_time)
    # 写入文件
    with open('example.txt', 'a') as file:
        file.write(f"[{current_time}]\t{name}\t{content}\n")

    # 唤醒失败计数+1，唤醒成功则清零
    if name == '005995' and end_time - start_time >= 22:
        wakeFailCount += 1
    elif name == '005995' and end_time - start_time < 22:
        wakeFailCount = 0

    print(f"wakeFailCount:{wakeFailCount}")

    # 唤醒失败次数累计超过4次时，重启设备
    if wakeFailCount >= 4:
        serial_bitstream('com8', '断电', 30)
        serial_bitstream('com8', '上电', 1)
        with open('example.txt', 'a') as file:
            file.write(f"[{current_time}] 重启设备\n")
        wakeFailCount = 0

    time.sleep(10)
    app.app_stop_()
    time.sleep(60)
