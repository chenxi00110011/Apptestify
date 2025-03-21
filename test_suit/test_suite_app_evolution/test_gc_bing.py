import configparser
from datetime import datetime
import time
import pytest
import uiautomator2_extended
from xrs_serial import serial_bitstream
from router_config import modify_wifi, read_config, router_management, get_sections
from adb_commands import AdbManager
from device_reset import reset

_config = read_config(r'C:\Users\Administrator\P2pServerTest\Apptestify\config\device_info.ini')
account_config = read_config(r'C:\Users\Administrator\P2pServerTest\Apptestify\config\base.ini')
parameter = [(account_config.get('睿博士正式服账号', '中国手机账户_1'),
              account_config.get('睿博士正式服账号', '中国手机密码_1'),
              _config.get('无线配网', 'did_1'),
              _config.get('无线配网', 'name_1')),
             # (account_config.get('睿博士正式服账号', '中国手机账户_1'),
             #  account_config.get('睿博士正式服账号', '中国手机密码_1'),
             #  _config.get('海思蓝牙', 'did_1'),
             #  _config.get('海思蓝牙', 'name_1'))
             ]


@pytest.mark.case_name("蓝牙配网绑定")
@pytest.mark.gcwl
@pytest.mark.test_environment
@pytest.mark.repeat(1)
@pytest.mark.parametrize("account, pwd, did, name", parameter)
# @pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_bing_bluetooth(account, pwd, did, name):
    # # 设备复位
    reset(did)
    time.sleep(30)

    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '广春物联')
    time.sleep(15)
    app.WAIT_TIME = 2.0
    app.go_to_page('蓝牙配网', "1234567890", "cx123456")

    count = 0
    start_time = time.time()

    while not app.exists_element(selector="text", value="设备添加成功") and count < 180:
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
    assert app.exists_element(selector='text', value='设备添加成功')


@pytest.mark.case_name("AP配网绑定")
@pytest.mark.gcwl
@pytest.mark.gc_ap
@pytest.mark.test_environment
@pytest.mark.repeat(1)
@pytest.mark.parametrize("account, pwd, did, name", parameter)
# @pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_bing_ap(account, pwd, did, name):
    # # 设备复位
    reset(did)
    time.sleep(30)

    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '广春物联')
    time.sleep(15)
    app.WAIT_TIME = 2.0
    app.go_to_page('AP配网', "1234567890", "cx123456", (f'ZWAP_{did}', '01234567'))

    count = 0
    start_time = time.time()

    while not app.exists_element(selector="text", value="设备添加成功") and count < 180:
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
    assert app.exists_element(selector='text', value='设备添加成功')


parameter = [('13638601129',
              'cx123456',
              'IOTFAA-303007-VDXCN',
              '303007'
              )]


@pytest.mark.case_name("扫码配网绑定")
@pytest.mark.gcwl
@pytest.mark.gc_qr
@pytest.mark.test_environment
@pytest.mark.repeat(1)
@pytest.mark.parametrize("account, pwd, did, name", parameter)
# @pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_bing_qr(account, pwd, did, name):
    # # 设备复位
    reset(did)
    time.sleep(30)

    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '广春物联')
    time.sleep(15)
    app.WAIT_TIME = 2.0
    app.go_to_page('扫码配网', "1234567890", "cx123456")

    count = 0
    start_time = time.time()

    while not app.exists_element(selector="text", value="设备添加成功") and count < 180:
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
    assert app.exists_element(selector='text', value='设备添加成功')
