import os
import threading
import time

import uiautomator2_extended
from uiautomator2_manager.adb_commands import AdbManager
from uiautomator2_manager.config_module import get_config
from uiautomator2 import connect

from xrs_serial import serial_bitstream


def device_reset():
    # 设备复位
    serial_bitstream('com4', '断电', 6)
    serial_bitstream('com4', '上电', 15)


# # 设备复位
device_reset()

# 启动睿博士app
app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
time.sleep(15)
app.go_to_page('首页', '13638601129', 'cx123456')
app.go_to_page('蓝牙-设备连接中', 'IOTFAA-000086-MRNRJ')
app.go_to_page('设备添加成功', 'Ruision-work-CS2.4', 'ruision2024@cs')