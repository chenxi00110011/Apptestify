import time
import uiautomator2_extended
from router_config import read_config
from file_operations import parse_log_entry
import pytest

account_config = read_config(r'..\..\config\base.ini')
device_config = read_config(r'..\..\config\device_info.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              device_config.get('云消息', 'did_1'),
              device_config.get('云消息', 'name_1'),
              )]


@pytest.mark.case_name("检查云消息")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.message
@pytest.mark.test_environment
@pytest.mark.repeat(1)
@pytest.mark.parametrize("account, pwd, did, name", parameter)
def test_get_event(account, pwd, did, name):
    # 启动睿博士app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(5)
    app.go_to_page('登录')
    app.go_to_page('首页', account, pwd)
    app.go_to_page("云消息", name)
    if app.exists_element(selector="text", value="消息通知功能未开启"):
        app.driver(text="立即开启").click()
        app.go_to_page("云消息", name)
    assert app.exists_element(selector="resource-id", value="com.zwcode.p6slite:id/push_tv_type")


config = read_config(r'..\..\config\base.ini')
parameter = [(config.get('睿博士测试手机账号', 'account'),
              config.get('睿博士测试手机账号', 'pwd'),
              config.get('RegexPatterns', 'date_pattern')
              )]


@pytest.mark.case_name("检查通知栏的消息")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.message
@pytest.mark.test_environment
@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, date_pattern", parameter)
def test_shangyun_push_message(account1, pwd1, date_pattern):
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("登录")
    app.go_to_page("首页", account1, pwd1)
    app.go_to_page("通知栏", "睿博士")
    time.sleep(10)
    count = 0
    while not app.exists_element(selector="text", value="睿博士") and count <= 600:
        count += 1
        time.sleep(1)

    count = 0
    while len(app.driver(resourceId="com.android.systemui:id/notification_text")) <= 1 and count <= 600:
        count += 1
        time.sleep(1)

    elements = app.driver(resourceId="com.android.systemui:id/notification_text")
    events = [element.get_text() for element in elements]

    # 判断2分钟内是否有事件上报
    assert time.time() - [parse_log_entry(event, date_pattern) for event in events][0] < 120

    app.go_to_page("关闭通知栏")
