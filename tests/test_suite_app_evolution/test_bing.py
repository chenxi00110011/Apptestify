import time
import pytest
import uiautomator2_extended
from xrs_serial import serial_bitstream


def device_reset():
    # 设备复位
    serial_bitstream('com4', '断电', 6)
    serial_bitstream('com4', '上电', 30)


def test_bing_ap():
    # 设备复位
    device_reset()

    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', '13638601129', 'cx123456')
    app.go_to_page('添加设备')
    app.go_to_page('AP热点配网')
    app.go_to_page('WLAN', 'Ruision-work-CS2.4', 'ruision2024@cs')
    app.go_to_page('设备连接中', 'ZWAP_IOTFAA-000086-MRNRJ')
