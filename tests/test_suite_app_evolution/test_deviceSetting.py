# test_deviceSetting.py

import time
import pytest
import uiautomator2_extended
from device_reset import reset
from router_config import modify_wifi, read_config, router_management, get_sections

WAIT_FOR_EVENT_WITH_TIMEOUT = 15

_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [
    # 国内手机账户转让设备
    (account_config.get('睿博士正式服账号', '中国手机账户_1'),
     account_config.get('睿博士正式服账号', '中国手机密码_1'),
     _config.get('设备设置', 'did_1'),
     _config.get('设备设置', 'name_1'),
     account_config.get('睿博士正式服账号', '中国区号')
     )
]


@pytest.mark.repeat(1)
@pytest.mark.case_name("打开人形侦测使能")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.setting
@pytest.mark.parametrize("account, pwd, did, name, areaCode", parameter)
def test_enableHumanDetection(account, pwd, did, name, areaCode):
    # 打开app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0

    app.go_to_page('登录')
    if not app.exists_element(selector="text", value="+86"):
        app.go_to_page("选择国家", areaCode)
    app.go_to_page('首页', account, pwd)
    app.go_to_page('报警管理', name)
    time.sleep(3)

    # 打开人形侦测使能
    app.title["checked"] = True
    app.go_to_page("人形侦测开关", "人形侦测报警")
    time.sleep(10)

    # 删除全部云消息
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('删除全部云消息', "我的")

    # 检查云消息是否上报人形侦测
    time.sleep(WAIT_FOR_EVENT_WITH_TIMEOUT)
    app.go_to_page('云消息', name)
    count = 0
    while not app.exists_element(selector="text", value="人形检测") and count < 10:
        app.driver(resourceId="com.zwcode.p6slite:id/common_title_left_layout").click()
        time.sleep(WAIT_FOR_EVENT_WITH_TIMEOUT)
        app.go_to_page('云消息', name)
        count += 1

    assert app.exists_element(selector="text", value="人形检测")


@pytest.mark.repeat(1)
@pytest.mark.case_name("关闭人形侦测使能")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.setting
@pytest.mark.parametrize("account, pwd, did, name, areaCode", parameter)
def test_disableHumanDetection(account, pwd, did, name, areaCode):
    # 打开app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('首页', account, pwd)
    app.go_to_page('报警管理', name)
    time.sleep(3)

    # 打开人形侦测使能
    app.title["checked"] = False
    app.go_to_page("人形侦测开关", "人形侦测报警")
    time.sleep(10)

    # 删除全部云消息
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('删除全部云消息', "我的")

    # 检查云消息是否上报人形侦测
    time.sleep(180)
    app.go_to_page('云消息', name)
    assert not app.exists_element(selector="text", value="人形检测")


@pytest.mark.repeat(1)
@pytest.mark.case_name("打开移动侦测使能")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.setting
@pytest.mark.parametrize("account, pwd, did, name, areaCode", parameter)
def test_enableMotionDetection(account, pwd, did, name, areaCode):
    # 打开app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('首页', account, pwd)
    app.go_to_page('报警管理', name)
    time.sleep(3)

    # 打开人形侦测使能
    app.title["checked"] = True
    app.go_to_page("移动侦测开关", "移动侦测报警")
    time.sleep(10)

    # 删除全部云消息
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('删除全部云消息', "我的")

    # 检查云消息是否上报人形侦测
    time.sleep(WAIT_FOR_EVENT_WITH_TIMEOUT)
    app.go_to_page('云消息', name)
    count = 0
    while not app.exists_element(selector="text", value="移动侦测") and count < 10:
        app.driver(resourceId="com.zwcode.p6slite:id/common_title_left_layout").click()
        time.sleep(WAIT_FOR_EVENT_WITH_TIMEOUT)
        app.go_to_page('云消息', name)
        count += 1

    assert app.exists_element(selector="text", value="移动侦测")


@pytest.mark.repeat(1)
@pytest.mark.case_name("关闭移动侦测使能")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.setting
@pytest.mark.parametrize("account, pwd, did, name, areaCode", parameter)
def test_disableMotionDetection(account, pwd, did, name, areaCode):
    # 打开app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('首页', account, pwd)
    app.go_to_page('报警管理', name)
    time.sleep(3)

    # 打开人形侦测使能
    app.title["checked"] = False
    app.go_to_page("移动侦测开关", "移动侦测报警")
    time.sleep(10)

    # 删除全部云消息
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('删除全部云消息', "我的")

    # 检查云消息是否上报人形侦测
    time.sleep(180)
    app.go_to_page('云消息', name)
    assert not app.exists_element(selector="text", value="移动侦测")


parameter = [
    # 国内手机账户转让设备
    (account_config.get('睿博士正式服账号', '中国手机账户_1'),
     account_config.get('睿博士正式服账号', '中国手机密码_1'),
     _config.get('设备设置', 'did_1'),
     _config.get('设备设置', 'name_1'),
     account_config.get('睿博士正式服账号', '中国区号'),
     "低"
     ),
    (account_config.get('睿博士正式服账号', '中国手机账户_1'),
     account_config.get('睿博士正式服账号', '中国手机密码_1'),
     _config.get('设备设置', 'did_1'),
     _config.get('设备设置', 'name_1'),
     account_config.get('睿博士正式服账号', '中国区号'),
     "中"
     ),
    (account_config.get('睿博士正式服账号', '中国手机账户_1'),
     account_config.get('睿博士正式服账号', '中国手机密码_1'),
     _config.get('设备设置', 'did_1'),
     _config.get('设备设置', 'name_1'),
     account_config.get('睿博士正式服账号', '中国区号'),
     "高"
     )
]


@pytest.mark.repeat(1)
@pytest.mark.case_name("设置人形侦测灵敏度")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.setting
@pytest.mark.parametrize("account, pwd, did, name, areaCode, sensitivity", parameter)
def test_setHumanDetectionSensitivity(account, pwd, did, name, areaCode, sensitivity):
    # 打开app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0

    app.go_to_page('登录')
    if not app.exists_element(selector="text", value="+86"):
        app.go_to_page("选择国家", areaCode)
    app.go_to_page('首页', account, pwd)
    app.go_to_page('报警管理', name)
    time.sleep(3)

    # 打开人形侦测使能
    app.title["checked"] = True
    app.go_to_page("人形侦测开关", "人形侦测报警")

    # 设置灵敏度，注意要打开使能才能显示
    app.go_to_page("设置灵敏度", sensitivity)

    # 删除全部云消息
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('删除全部云消息', "我的")

    # 检查云消息是否上报人形侦测
    time.sleep(WAIT_FOR_EVENT_WITH_TIMEOUT)
    app.go_to_page('云消息', name)
    count = 0
    while not app.exists_element(selector="text", value="人形检测") and count < 10:
        app.driver(resourceId="com.zwcode.p6slite:id/common_title_left_layout").click()
        time.sleep(WAIT_FOR_EVENT_WITH_TIMEOUT)
        app.go_to_page('云消息', name)
        count += 1

    assert app.exists_element(selector="text", value="人形检测")


@pytest.mark.repeat(1)
@pytest.mark.case_name("设置移动侦测灵敏度")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.setting
@pytest.mark.parametrize("account, pwd, did, name, areaCode, sensitivity", parameter)
def test_setMotionDetectionSensitivity(account, pwd, did, name, areaCode, sensitivity):
    # 打开app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0

    app.go_to_page('登录')
    if not app.exists_element(selector="text", value="+86"):
        app.go_to_page("选择国家", areaCode)
    app.go_to_page('首页', account, pwd)
    app.go_to_page('报警管理', name)
    time.sleep(3)

    # 打开人形侦测使能
    app.title["checked"] = True
    app.go_to_page("移动侦测开关", "移动侦测报警")

    # 设置灵敏度，注意要打开使能才能显示
    app.go_to_page("设置灵敏度", sensitivity)

    # 删除全部云消息
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('删除全部云消息', "我的")

    # 检查云消息是否上报人形侦测
    time.sleep(WAIT_FOR_EVENT_WITH_TIMEOUT)
    app.go_to_page('云消息', name)
    count = 0
    while not app.exists_element(selector="text", value="移动侦测") and count < 10:
        app.driver(resourceId="com.zwcode.p6slite:id/common_title_left_layout").click()
        time.sleep(WAIT_FOR_EVENT_WITH_TIMEOUT)
        app.go_to_page('云消息', name)
        count += 1

    assert app.exists_element(selector="text", value="移动侦测")


parameter = [
    # 国内手机账户转让设备
    (account_config.get('睿博士正式服账号', '中国手机账户_1'),
     account_config.get('睿博士正式服账号', '中国手机密码_1'),
     _config.get('设备设置', 'did_1'),
     _config.get('设备设置', 'name_1'),
     account_config.get('睿博士正式服账号', '中国区号'),
     {
         "eventName": "移动侦测",
         "eventType": "移动侦测"
     }
     ),
    (account_config.get('睿博士正式服账号', '中国手机账户_1'),
     account_config.get('睿博士正式服账号', '中国手机密码_1'),
     _config.get('设备设置', 'did_1'),
     _config.get('设备设置', 'name_1'),
     account_config.get('睿博士正式服账号', '中国区号'),
     {
         "eventName": "人形侦测",
         "eventType": "人形检测"
     }
     )
]


@pytest.mark.repeat(1)
@pytest.mark.case_name("设置布防区域")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.setting
@pytest.mark.parametrize("account, pwd, did, name, areaCode, eventKind", parameter)
def test_setupMonitoringArea(account, pwd, did, name, areaCode, eventKind):
    # 打开app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('首页', account, pwd)
    app.go_to_page('报警管理', name)
    time.sleep(3)

    # 打开人形侦测使能
    app.title["checked"] = True
    app.go_to_page("移动侦测开关", f"{eventKind['eventName']}报警")

    # 设置布防区域
    app.go_to_page("侦测区域设置", 0.9)

    # 删除全部云消息
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('删除全部云消息', "我的")

    # 检查云消息是否上报人形侦测
    time.sleep(WAIT_FOR_EVENT_WITH_TIMEOUT)
    app.go_to_page('云消息', name)
    count = 0
    while not app.exists_element(selector="text", value=eventKind['eventType']) and count < 10:
        app.driver(resourceId="com.zwcode.p6slite:id/common_title_left_layout").click()
        time.sleep(WAIT_FOR_EVENT_WITH_TIMEOUT)
        app.go_to_page('云消息', name)
        count += 1

    assert app.exists_element(selector="text", value=eventKind['eventType'])


parameter = [
    # 国内手机账户转让设备
    (account_config.get('睿博士正式服账号', '中国手机账户_1'),
     account_config.get('睿博士正式服账号', '中国手机密码_1'),
     _config.get('设备设置', 'did_1'),
     _config.get('设备设置', 'name_1'),
     account_config.get('睿博士正式服账号', '中国区号'),
     "春眠不觉晓,ABCabc123"
     )
]


@pytest.mark.repeat(1)
@pytest.mark.case_name("设置OSD")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.setting
@pytest.mark.parametrize("account, pwd, did, name, areaCode, osd", parameter)
def setOSDParameters(account, pwd, did, name, areaCode, osd):
    # 打开app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('首页', account, pwd)
    app.go_to_page('设备信息', name)
    app.title["checked"] = True
    app.go_to_page('OSD设置', osd, "显示通道名")

    assert app.exists_element(selector="resource-id", value="com.zwcode.p6slite:id/osd_name_text")
    assert app.driver(resourceId="com.zwcode.p6slite:id/osd_name_text").get_text() == osd


parameter = [
    # 国内手机账户转让设备
    (account_config.get('睿博士正式服账号', '中国手机账户_1'),
     account_config.get('睿博士正式服账号', '中国手机密码_1'),
     _config.get('设备设置', 'did_1'),
     _config.get('设备设置', 'name_1'),
     account_config.get('睿博士正式服账号', '中国区号'),
     True
     ),
    # 国内手机账户转让设备
    (account_config.get('睿博士正式服账号', '中国手机账户_1'),
     account_config.get('睿博士正式服账号', '中国手机密码_1'),
     _config.get('设备设置', 'did_1'),
     _config.get('设备设置', 'name_1'),
     account_config.get('睿博士正式服账号', '中国区号'),
     False
     )
]


@pytest.mark.repeat(1)
@pytest.mark.case_name("OSD显示通道名使能")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.setting
@pytest.mark.parametrize("account, pwd, did, name, areaCode, checked", parameter)
def test_displayOSDChannelName(account, pwd, did, name, areaCode, checked):
    # 打开app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('首页', account, pwd)
    app.go_to_page('设备信息', name)
    app.title["checked"] = checked
    app.go_to_page('OSD使能开关', "显示通道名")
    time.sleep(5)

    # 检查OSD显示状态
    if checked:
        assert app.exists_element(selector="resource-id", value="com.zwcode.p6slite:id/osd_name_text")
    else:
        assert not app.exists_element(selector="resource-id", value="com.zwcode.p6slite:id/osd_name_text")


@pytest.mark.repeat(1)
@pytest.mark.case_name("OSD显示时间使能")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.setting_test
@pytest.mark.parametrize("account, pwd, did, name, areaCode, checked", parameter)
def test_displayOSDTime(account, pwd, did, name, areaCode, checked):
    # 打开app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('首页', account, pwd)
    app.go_to_page('设备信息', name)
    app.title["checked"] = checked
    app.go_to_page('OSD使能开关', "显示时间")
    time.sleep(5)

    # 检查OSD显示状态
    if checked:
        assert app.exists_element(selector="resource-id", value="com.zwcode.p6slite:id/osd_time_text")
    else:
        assert not app.exists_element(selector="resource-id", value="com.zwcode.p6slite:id/osd_time_text")


