import os.path
import time
import pytest
import uiautomator2_extended
from adb_commands import AdbManager
from config_module import get_config

qrcodes = [
    ('v1.png', '001494'),
    ('v2.png', '001494'),
    ('v3.png', '001494'),
    ('v4.png', '000000'),
    ('v5.png', '303007'),
    ('v6.jpg', '000000'),
    ('v7.png', '000000')
]


def get_share_qrcode(dev_name):
    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(30)
    app.go_to_page('登录')
    app.go_to_page('首页', '13638601129', 'cx123456')
    app.go_to_page('展示分享二维码', dev_name)
    app.driver.screenshot(filename="../../data/qr/v5.png")
    app.app_stop_()


@pytest.mark.parametrize("qrcode ,dev_name", qrcodes)
@pytest.mark.repeat(10)
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
    app.go_to_page('首页', '18086409233', 'cx123456')
    print("#" * 200, dev_name)
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
