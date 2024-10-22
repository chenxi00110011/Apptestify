import time
import pytest
import uiautomator2_extended
from xrs_serial import serial_bitstream
from router_config import modify_wifi, read_config, router_management, get_sections
from adb_commands import AdbManager


def device_reset():
    config = read_config(r'..\..\config\base.ini')
    com = config.get("串口", "reset")
    # 设备复位
    serial_bitstream(com, '断电', 6)
    serial_bitstream(com, '上电', 30)


_config = read_config(r'..\..\config\device_info.ini')
parameter = [(_config.get('设备分享', 'did'), _config.get('设备分享', 'name'))]


@pytest.mark.repeat(100)
@pytest.mark.parametrize("did,name", parameter)
def test_handoverDevice(did, name):
    # 设备复位
    device_reset()

    # 添加设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('登录')
    app.go_to_page('首页', '18086409233', 'cx123456')
    if app.exists_element(selector='text', value=name):
        app.go_to_page('删除设备', name)
    app.go_to_page('手动添加', did, name)

    # 转让设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('首页', '18086409233', 'cx123456')
    app.go_to_page('转让设备', name, '分享管理', '13638601129')

    # 收受设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', '13638601129', 'cx123456')
    app.go_to_page('接受')
    assert app.exists_element(selector='text', value=name)
