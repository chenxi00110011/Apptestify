import configparser
import time
import pytest
import uiautomator2_extended
from xrs_serial import serial_bitstream
from router_config import modify_wifi, read_config, router_management, get_sections
from adb_commands import AdbManager
from device_reset import reset

_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              _config.get('云存储设备', 'did'),
              _config.get('云存储设备', 'name')
              )
             ]


@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name", parameter)
def test_enable_store_switch(account1, pwd1, did, name):
    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', '18086409233', 'cx123456')
    assert app.exists_element(selector='text', value=name)

    # 打开云存储
    app.title["checked"] = True
    app.go_to_page("云存储开关", name)
    time.sleep(300)

    # 关闭云存储
    app.title["checked"] = False
    app.go_to_page("云存储开关")
    time.sleep(300)

    # 打开云存储
    app.title["checked"] = True
    app.go_to_page("云存储开关")
    time.sleep(300)

    # 云回放截图
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("云回放", name)
    app.go_to_page("截图")
