import time
import pytest
import uiautomator2_extended
from router_config import read_config
import uiautomator2 as u2
from datetime import datetime, timezone, timedelta
import inspect

_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              _config.get('4G设备', 'did_1'),
              _config.get('4G设备', 'name_1')
              )]


@pytest.mark.case_name("测试在中国服环境下，设备正常显示4G图标")
@pytest.mark.repeat(1)
@pytest.mark.dev_4g
@pytest.mark.test_environment
@pytest.mark.parametrize("account1, pwd1, did, name", parameter)
def test_4g_icon_display_on_china_server(account1, pwd1, did, name):
    """
    测试在中国服环境下，设备正常显示4G图标。
    """
    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 0.5
    app.go_to_page('登录')
    app.go_to_page('首页', account1, pwd1)
    time.sleep(5)
    app.swipe_until_element_visible(name,
                                    rectangle=app.run_parameters.get('rectangle'))
    # 检查页面是否显示4G图标
    assert app.exists_element(selector="text", value="4G流量")
