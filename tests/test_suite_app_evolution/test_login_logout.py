import time
import pytest
import uiautomator2_extended
from xrs_serial import serial_bitstream
from mailbox_reader import get_verification_code


def test_logout_email():
    # 启动睿博士appblue
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', 'chenxi11001111@163.com', 'cx123456')
    app.go_to_page('注销账号')
    app.go_to_page('获取验证码')
    code = get_verification_code()
    app.go_to_page('完成注销', code)


def test_register_email():
    # 启动睿博士appblue
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('获取验证码', 'chenxi11001111@163.com')
    code = get_verification_code()
    app.go_to_page('注册邮箱', code, "cx123456", "cx123456")
    time.sleep(3)
