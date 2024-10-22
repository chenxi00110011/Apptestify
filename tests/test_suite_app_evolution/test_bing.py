import configparser
import time
import pytest
import uiautomator2_extended
from xrs_serial import serial_bitstream
from router_config import modify_wifi, read_config, router_management, get_sections
from adb_commands import AdbManager


def device_reset():
    config = read_config(r'C:\Users\Administrator\P2pServerTest\Apptestify\config\base.ini')
    com = config.get("串口", "reset")
    # 设备复位
    serial_bitstream(com, '断电', 6)
    serial_bitstream(com, '上电', 30)


@pytest.mark.repeat(20)
def test_bing_ap():
    # 设备复位
    device_reset()

    # 启动睿博士appblue
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', '13638601129', 'cx123456')
    app.go_to_page('添加设备')
    app.go_to_page('AP热点配网')
    app.go_to_page('WLAN', 'Ruision-work-CS2.4', 'ruision2024@cs')
    app.go_to_page('截图', 'ZWAP_IOTFAA-000086-MRNRJ')
    time.sleep(10)
    assert app.exists_element(selector='text', value='设备添加成功')


@pytest.mark.repeat(20)
def test_bing_wifi_qr():
    # # 设备复位
    device_reset()

    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', '13638601129', 'cx123456')
    app.go_to_page('添加设备')
    app.go_to_page('扫码配网')
    app.go_to_page('输入WiFi网络')
    if not app.exists_element(selector='text', value='Ruision-work-CS2.4'):
        app.go_to_page('更换WIFI', 'Ruision-work-CS2.4')
    app.go_to_page('设备扫描二维码', 'Ruision-work-CS2.4', 'ruision2024@cs')
    time.sleep(3)
    app.go_to_page('设备添加成功')
    assert app.exists_element(selector='text', value='设备添加成功')


@pytest.mark.repeat(1)
# @pytest.mark.flaky(reruns=20, reruns_delay=5)
def test_bing_bluetooth():
    # # 设备复位
    device_reset()

    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', '13638601129', 'cx123456')
    app.go_to_page('输入WiFi网络', 'IOTFAA-000086-MRNRJ')
    time.sleep(5)
    app.go_to_page('设备添加成功', 'Ruision-work-CS2.4', 'ruision2024@cs')
    # if app.exists_element(selector='text', value='设备添加失败'):
    #     time.sleep(3600*24)
    assert app.exists_element(selector='text', value='设备添加成功')


@pytest.mark.parametrize("section", get_sections(r'..\..\config\router.ini'))
def test_various_ssid_bluetooth(section):
    # 设备复位
    device_reset()

    # 设置路由器ssid和密码
    print("本次测试路由器的SSID类型：\t", section)
    config_path = r'..\..\config\router.ini'

    # 读取配置
    config = read_config(config_path)
    _url = config.get(section, "url")
    _login_password = config.get(section, "login_password")
    _ssid = config.get(section, "ssid")
    _pwd = config.get(section, "wifi_password")

    # 执行管理操作
    router_management(_url, _login_password, _ssid, _pwd)

    # 手机连接Wi-Fi
    AdbManager.connect_network('H675FIS8JJU8AMWW', _ssid, _pwd)

    # 启动手机app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', '13638601129', 'cx123456')
    app.go_to_page('输入WiFi网络', 'IOTFAA-000086-MRNRJ')
    time.sleep(5)
    app.go_to_page('设备添加成功', _ssid, _pwd)
    # if app.exists_element(selector='text', value='设备添加失败'):
    #     time.sleep(3600*24)
    assert app.exists_element(selector='text', value='设备添加成功')


@pytest.mark.parametrize("section", get_sections(r'..\..\config\router.ini'))
def test_various_ssid_ap(section):
    # 设备复位
    device_reset()

    # 设置路由器ssid和密码
    print("本次测试路由器的SSID类型：\t", section)
    config_path = r'..\..\config\router.ini'

    # 读取配置
    config = read_config(config_path)
    _url = config.get(section, "url")
    _login_password = config.get(section, "login_password")
    _ssid = config.get(section, "ssid")
    _pwd = config.get(section, "wifi_password")

    # 执行管理操作
    router_management(_url, _login_password, _ssid, _pwd)

    # 手机连接Wi-Fi
    AdbManager.connect_network('H675FIS8JJU8AMWW', _ssid, _pwd)

    # 启动睿博士appblue
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', '13638601129', 'cx123456')
    app.go_to_page('添加设备')
    app.go_to_page('AP热点配网')
    app.go_to_page('WLAN', _ssid, _pwd)
    app.go_to_page('截图', ('ZWAP_IOTFAA-000086-MRNRJ', '01234567'), (_ssid, _pwd))
    time.sleep(10)
    assert app.exists_element(selector='text', value='设备添加成功')


@pytest.mark.parametrize("section", get_sections(r'..\..\config\router.ini'))
def test_various_ssid_qr(section):
    # 设备复位
    device_reset()

    # 设置路由器ssid和密码
    print("本次测试路由器的SSID类型：\t", section)
    config_path = r'..\..\config\router.ini'

    # 读取配置
    config = read_config(config_path)
    _url = config.get(section, "url")
    _login_password = config.get(section, "login_password")
    _ssid = config.get(section, "ssid")
    _pwd = config.get(section, "wifi_password")

    # 执行管理操作
    router_management(_url, _login_password, _ssid, _pwd)

    # 手机连接Wi-Fi
    AdbManager.connect_network('H675FIS8JJU8AMWW', _ssid, _pwd)

    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', '13638601129', 'cx123456')
    app.go_to_page('添加设备')
    app.go_to_page('扫码配网')
    app.go_to_page('输入WiFi网络')
    if not app.exists_element(selector='text', value=_ssid):
        app.go_to_page('更换WIFI', _ssid)
    app.go_to_page('设备扫描二维码', _ssid, _pwd)
    time.sleep(3)
    app.go_to_page('设备添加成功')
    assert app.exists_element(selector='text', value='设备添加成功')
