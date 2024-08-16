import time
import pytest
import uiautomator2_extended
from xrs_serial import serial_bitstream


def device_reset():
    # 设备复位
    serial_bitstream('com4', '断电', 6)
    serial_bitstream('com4', '上电', 30)


@pytest.mark.repeat(50)
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
    app.go_to_page('截图', 'ZWAP_IOTFAA-000086-MRNRJ')
    time.sleep(10)
    assert app.exists_element(selector='text', value='设备添加成功')


@pytest.mark.repeat(1)
def test_bing_wifi_qr():
    # 设备复位
    device_reset()

    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)


@pytest.mark.repeat(1)
def test_bing_bluetooth():
    # 设备复位
    device_reset()

    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('蓝牙-设备连接中', 'IOTFAA-000086-MRNRJ')
    app.go_to_page('设备添加成功', 'Ruision-work-CS2.4', 'ruision2024@cs')