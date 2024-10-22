import time
import pytest
import uiautomator2_extended
from xrs_serial import serial_bitstream
from device_api import DeviceAPIManager

resolutions = ['高清', '标清', '超清', ]


def device_reset():
    # 设备复位
    serial_bitstream('com4', '断电', 6)
    serial_bitstream('com4', '上电', 30)


@pytest.mark.repeat(1)
@pytest.mark.parametrize("resolution", resolutions)
def test_switch_resolution(resolution: str):
    DeviceAPIManager(mac='5A:5A:00:81:47:28').dev_reboot()
    time.sleep(30)
    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', '13638601129', 'cx123456')
    app.go_to_page('直播', '办公室')
    time.sleep(5)
    app.go_to_page('切换画质', resolution)
    time.sleep(5)
    app.go_to_page('截图')
    app.app_stop_()
