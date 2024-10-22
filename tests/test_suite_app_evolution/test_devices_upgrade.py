import configparser
import time
import pytest
import uiautomator2_extended
from xrs_serial import serial_bitstream
from router_config import modify_wifi, read_config, router_management, get_sections
from adb_commands import AdbManager


@pytest.mark.parametrize("name", [read_config(r'..\..\config\device_info.ini').get('W43T-46PHM-S/LW/BT', 'name')])
def test_ipc_upgrade(name):
    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', '18086409233', 'cx123456')
    app.go_to_page('固件更新', name, '固件更新')
    assert app.exists_element(selector='text', value='升级成功')


@pytest.mark.parametrize("name", [read_config(r'..\..\config\device_info.ini').get('NBD-3016NEA', 'name')])
def test_nvr_upgrade(name):
    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', '18086409233', 'cx123456')
    app.go_to_page('版本升级', name)
