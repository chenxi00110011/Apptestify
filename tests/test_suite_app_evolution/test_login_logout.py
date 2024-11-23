import time
import pytest
import uiautomator2_extended
from router_config import read_config
from xrs_serial import serial_bitstream
from mailbox_reader import get_verification_code

_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试邮箱账号', 'account'),
              account_config.get('睿博士测试邮箱账号', 'pwd')
              )]


@pytest.mark.login_logout
@pytest.mark.repeat(1)
@pytest.mark.parametrize("account, pwd", parameter)
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_logout_email(account, pwd):
    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account, pwd)
    app.go_to_page('注销账号')
    app.go_to_page('获取验证码')
    code = get_verification_code()
    app.go_to_page('完成注销', code)


@pytest.mark.login_logout
@pytest.mark.repeat(1)
@pytest.mark.parametrize("account, pwd", parameter)
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_register_email(account, pwd):
    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('获取验证码', account)
    code = get_verification_code()
    app.go_to_page('注册邮箱', code, pwd, pwd)
    time.sleep(3)
