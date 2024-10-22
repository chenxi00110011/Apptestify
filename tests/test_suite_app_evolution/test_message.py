import time
import pytest
import uiautomator2_extended
from xrs_serial import serial_bitstream
from mailbox_reader import get_verification_code


def test_get_event():
    # 启动睿博士appblue
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(5)
    # app.go_to_page('登录')
    app.go_to_page('首页', '18086409233', 'cx123456')
    app.go_to_page("云消息", "355259")
    assert app.exists_element(selector="resource-id", value="com.zwcode.p6slite:id/push_tv_type")
