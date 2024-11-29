import os.path
import time
import pytest

import ntp_util
import uiautomator2_extended
from adb_commands import AdbManager
from config_module import get_config
from router_config import read_config
from image_popup import show_image
import threading
from device_reset import reset

qrcodes = [
    ('v1.png', '001494'),
    ('v2.png', '001494'),
    ('v3.png', '001494'),
    ('v4.png', '000000'),
    ('v5.png', '303007'),
    ('v6.jpg', '000000'),
    ('v7.png', '000000')
]

_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              _config.get('4G设备', 'did_2'),
              _config.get('4G设备', 'name_2')
              )]


def get_share_qrcode(dev_name):
    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(30)
    app.go_to_page('登录')
    app.go_to_page('首页', account_config.get('睿博士测试手机账号', 'account'),
                   account_config.get('睿博士测试手机账号', 'pwd'))
    app.go_to_page('展示分享二维码', dev_name)
    app.driver.screenshot(filename="../../data/qr/v5.png")
    app.app_stop_()


@pytest.mark.skip(reason="这个测试用例暂时不需要执行")
@pytest.mark.parametrize("qrcode ,dev_name", qrcodes)
@pytest.mark.repeat(1)
def test_scan_v1_code(qrcode: str, dev_name: str):
    """
    测试步骤：
    1.下载二维码到手机相册
    2.进入app>>扫一扫添加>>选择本地相册中的二维码
    3.检查页面是否跳转到添加成功
    """
    if qrcode == 'v5.png':
        get_share_qrcode(dev_name)
    # 下载V1二维码
    AdbManager.download_file(
        deviceID='H675FIS8JJU8AMWW',
        local_path=os.path.join(get_config('睿博士').QR_DIR, qrcode),
        remote_path=os.path.join(get_config('睿博士').MOBILE_SCREEN_CAPTUREA, 'test.png')
    )

    # 重启手机，使相册加载二维码图片
    AdbManager.execute_command(
        deviceID='H675FIS8JJU8AMWW',
        command=AdbManager.REBOOT
    )
    time.sleep(60)

    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(10)
    app.go_to_page('登录')
    app.go_to_page('首页', account_config.get('睿博士测试手机账号', 'account'),
                   account_config.get('睿博士测试手机账号', 'pwd'))
    if app.exists_element(selector="text", value=dev_name):
        app.go_to_page('删除设备', dev_name)
    app.go_to_page('扫一扫')
    app.go_to_page('等待添加')
    time.sleep(60)
    if qrcode in ['v1.png', 'v2.png', 'v3.png']:
        assert app.exists_element(selector="text", value='设备添加成功')
    elif qrcode == 'v4.png':
        assert app.exists_element(selector="text", value='临时密码')
    elif qrcode == 'v5.png':
        app.driver(text="去连接").click()
        time.sleep(2)
        assert app.exists_element(selector="text", value='收到分享的结果')
        assert app.exists_element(selector="text", value='成功接受分享')
    elif qrcode in ['v6.jpg', 'v7.png']:
        assert app.exists_element(selector="text", value='桌面版确认登录')
        assert app.exists_element(selector="text", value='登录')


def show_image_in_thread(image_path, display_time):
    thread = threading.Thread(target=show_image, args=(image_path, display_time))
    thread.start()


qrcodes = [
    ('v1.png', _config.get('4G设备', 'name_2'), _config.get('4G设备', 'did_2')),
    ('v2.png', _config.get('4G设备', 'name_2'), _config.get('4G设备', 'did_2')),
    ('v3.png', _config.get('4G设备', 'name_2'), _config.get('4G设备', 'did_2')),
    ('v3-1.png', _config.get('4G设备', 'name_2'), _config.get('4G设备', 'did_2'))
]


@pytest.mark.case_name("扫描v1v2v3码")
@pytest.mark.scanqr
@pytest.mark.test_environment
@pytest.mark.parametrize("qrcode, dev_name, did", qrcodes)
@pytest.mark.repeat(1)
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_scan_device_qr_code(qrcode, dev_name, did):
    # 设备复位
    reset(did)
    time.sleep(60)

    # 第一步打开app，进入扫一扫
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account_config.get('睿博士测试手机账号', 'account'),
                   account_config.get('睿博士测试手机账号', 'pwd'))
    if app.exists_element(selector="text", value=dev_name):
        app.go_to_page('删除设备', dev_name)
        time.sleep(5)

    app.go_to_page('蓝牙搜索')

    # 电脑桌面弹出图片
    photo_path = os.path.join(get_config('睿博士').QR_DIR, qrcode)
    print(f"Photo path: {photo_path}")
    assert os.path.exists(photo_path), f"File not found at {photo_path}"
    show_image_in_thread(photo_path, 5000)

    # 检查是否添加成功
    count = 0
    start_time = int(time.time())
    while not app.exists_element(selector="text", value='设备添加成功') and count < 60:
        count += 1
        time.sleep(1)
    end_time = int(time.time())
    app.title['shootName'] = ntp_util.timestamp_to_date(format="%H-%M-%S", today=0) + str(
        end_time - start_time) + qrcode
    app.save_screenshotV1()
    assert app.exists_element(selector="text", value='设备添加成功')


qrcodes = [
    ('v4.png', _config.get('4G设备', 'name_2'), _config.get('4G设备', 'did_2')),
]


@pytest.mark.case_name("扫码生成临时密码")
@pytest.mark.scanqr
@pytest.mark.test_environment
@pytest.mark.parametrize("qrcode, dev_name, did", qrcodes)
@pytest.mark.repeat(1)
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_scan_qr_for_temp_password(qrcode, dev_name, did):
    # 第一步打开app，进入扫一扫
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account_config.get('睿博士测试手机账号', 'account'),
                   account_config.get('睿博士测试手机账号', 'pwd'))

    app.go_to_page('蓝牙搜索')

    # 电脑桌面弹出图片
    photo_path = os.path.join(get_config('睿博士').QR_DIR, qrcode)
    print(f"Photo path: {photo_path}")
    assert os.path.exists(photo_path), f"File not found at {photo_path}"
    show_image_in_thread(photo_path, 5000)

    # 检查是否添加成功
    count = 0
    start_time = int(time.time())
    while not app.exists_element(selector="text", value='临时密码') and count < 60:
        count += 1
        time.sleep(1)
    end_time = int(time.time())
    app.title['shootName'] = ntp_util.timestamp_to_date(format="%H-%M-%S", today=0) + str(
        end_time - start_time) + qrcode
    app.save_screenshotV1()
    assert app.exists_element(selector="text", value='临时密码')


qrcodes = [
    ('v6.jpg', _config.get('4G设备', 'name_2'), _config.get('4G设备', 'did_2')),
    ('v7.png', _config.get('4G设备', 'name_2'), _config.get('4G设备', 'did_2'))
]


@pytest.mark.case_name("扫码登录NVR和VMS")
@pytest.mark.scanqr
@pytest.mark.test_environment
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.parametrize("qrcode, dev_name, did", qrcodes)
def test_scan_qr_to_login(qrcode, dev_name, did):
    # 第一步打开app，进入扫一扫
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account_config.get('睿博士测试手机账号', 'account'),
                   account_config.get('睿博士测试手机账号', 'pwd'))

    app.go_to_page('蓝牙搜索')

    # 电脑桌面弹出图片
    photo_path = os.path.join(get_config('睿博士').QR_DIR, qrcode)
    print(f"Photo path: {photo_path}")
    assert os.path.exists(photo_path), f"File not found at {photo_path}"
    show_image_in_thread(photo_path, 5000)

    # 检查是否添加成功
    count = 0
    start_time = int(time.time())
    while not app.exists_element(selector="text", value='桌面版确认登录') and count < 60:
        count += 1
        time.sleep(1)
    end_time = int(time.time())
    app.title['shootName'] = ntp_util.timestamp_to_date(format="%H-%M-%S", today=0) + str(
        end_time - start_time) + qrcode
    app.save_screenshotV1()
    assert app.exists_element(selector="text", value='桌面版确认登录')


qrcodes = [
    ('v5.png', _config.get('设备分享', 'name_1'), _config.get('设备分享', 'did_1')),
]


@pytest.mark.case_name("扫码分享设备")
@pytest.mark.scanqr
@pytest.mark.test_environment
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.parametrize("qrcode, name, did", qrcodes)
def test_qr_code_share_device(qrcode, name, did):
    # 设备复位
    reset(did)

    # 添加设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("登录")
    app.go_to_page('首页', account_config.get('睿博士测试手机账号', 'account'),
                   account_config.get('睿博士测试手机账号', 'pwd'))
    app.go_to_page('输入WiFi网络', did)
    time.sleep(5)
    app.go_to_page('设备添加成功', 'Ruision-work-CS2.4', 'ruision2024@cs')
    assert app.exists_element(selector='text', value='设备添加成功')

    # 分享设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('首页', account_config.get('睿博士测试手机账号', 'account'),
                   account_config.get('睿博士测试手机账号', 'pwd'))
    app.go_to_page('二维码', name, '分享管理')

    # 截图
    bounds = app.driver(resourceId="com.zwcode.p6slite:id/qr_iv").info["bounds"]
    photo_path = app.save_screenshotV1(bounds)

    # 扫描分享二维码
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account_config.get('睿博士测试手机备用账号', 'account'),
                   account_config.get('睿博士测试手机备用账号', 'pwd'))

    app.go_to_page('蓝牙搜索')

    # 电脑桌面弹出图片
    print(f"Photo path: {photo_path}")
    assert os.path.exists(photo_path), f"File not found at {photo_path}"
    show_image_in_thread(photo_path, 5000)

    time.sleep(3)
    app.driver(text="去连接").click()

    # 检查是否已成功分享
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    assert app.exists_element(selector='text', value=name)
