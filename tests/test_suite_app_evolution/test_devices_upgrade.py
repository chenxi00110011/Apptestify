import configparser
import time
import pytest
import uiautomator2_extended
from device_reset import reset
from xrs_serial import serial_bitstream
from router_config import modify_wifi, read_config, router_management, get_sections
from adb_commands import AdbManager

_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              _config.get('无线配网', 'did_1'),
              _config.get('无线配网', 'name_1')
              )]


@pytest.mark.repeat(1)
@pytest.mark.case_name("ipc云升级")
@pytest.mark.share
@pytest.mark.test_environment
@pytest.mark.parametrize("account, pwd, did, name", parameter)
def test_ipc_upgrade(account, pwd, did, name):
    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account, pwd)
    if not app.exists_element(selector="text", value=name):
        # 设备复位
        reset(did)
        time.sleep(30)

        # 添加设备
        app.go_to_page('输入WiFi网络', did)
        time.sleep(5)
        app.go_to_page('设备添加成功', 'Ruision-work-CS2.4', 'ruision2024@cs')
        assert app.exists_element(selector='text', value='设备添加成功')

    app.go_to_page('固件更新', name, '固件更新')
    assert app.exists_element(selector='text', value='升级成功')


_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              _config.get('NVR升级', 'did'),
              _config.get('NVR升级', 'name')
              )]


@pytest.mark.repeat(1)
@pytest.mark.case_name("nvr云升级")
@pytest.mark.share
@pytest.mark.test_environment
@pytest.mark.parametrize("account, pwd, did, name", parameter)
def test_nvr_upgrade(account, pwd, did, name):
    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account, pwd)
    app.go_to_page('版本升级', name)
