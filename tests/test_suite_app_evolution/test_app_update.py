import time
import pytest
import uiautomator2_extended
from router_config import read_config
import uiautomator2 as u2
from datetime import datetime, timezone, timedelta
import inspect

account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd')
              )
             ]


@pytest.mark.repeat(1)
@pytest.mark.test_environment
@pytest.mark.parametrize("account1, pwd1", parameter)
def test_app_update(account1, pwd1):
    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    # app.go_to_page('登录')
    app.go_to_page('首页', '18086409233', 'cx123456')

    # 检查升级弹窗
    app.exists_element(selector="text", value="发现新版本啦")
    app.exists_element(selector="text", value="1、已是最新版本1\n2、已是最新版本2\n3、已是最新版本3\n4、已是最新版本4（简体）")
    app.exists_element(selector="text", value="立即体验")
    app.exists_element(selector="text", value="暂不升级")
    app.exists_element(selector="text", value="下次不再提醒")

    # app升级
