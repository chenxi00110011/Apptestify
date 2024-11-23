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
              _config.get('云存储设备', 'did'),
              _config.get('云存储设备', 'name')
              )]


# 验证云存开关是否有效
@pytest.mark.repeat(1)
@pytest.mark.parametrize("account, pwd, did, name", parameter)
def test_enableCloudSwitch(account, pwd, did, name):
    # 用例名称
    case_name = "云录像关闭与开启"

    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account, pwd)

    # 打开云存储
    app.title["checked"] = True
    app.go_to_page("云存储开关", name)
    time.sleep(120)

    # 关闭云存储
    app.title["checked"] = False
    app.go_to_page("云存储开关")
    time.sleep(600)

    # 打开云存储
    app.title["checked"] = True
    app.go_to_page("云存储开关")
    time.sleep(600)

    # 云回放截图
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("云回放", name)
    time.sleep(5)

    # 截图
    app.title["shootName"] = case_name + str(int(time.time()) % 10000) + ".jpg"
    app.save_screenshotV1()


# 录制云存视频，并通过微信分享
@pytest.mark.parametrize("account1, pwd1, did, name", parameter)
def test_cloudRecordAndShare(account1, pwd1, did, name):
    # 登录并进入云回放页面
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("登录")
    app.go_to_page("首页", account1, pwd1)
    app.go_to_page("云回放", name)

    # 录制1分钟
    app.go_to_page("云回放录制")
    time.sleep(60)
    app.go_to_page("云回放录制")

    # 进入相册，微信分享给朋友
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("微信分享录像")

    # 进入微信，查看录像
    d = u2.connect('H675FIS8JJU8AMWW')  # 如果只有一个设备，可以省略参数
    d.app_start('com.tencent.mm')
    # 等待微信主界面加载
    d(resourceId="com.tencent.mm:id/b5l").wait(timeout=10.0)
    # 进入聊天框
    d(text="陈熙").click()
    # 检查录像是否存在
    assert app.exists_element(selector="resource-id", value="com.tencent.mm:id/oy_")

    # 清空聊天记录
    app.driver(resourceId="com.tencent.mm:id/coz").click()
    app.driver(text="清空聊天记录").click()
    app.driver(text="清空").click()


@pytest.mark.parametrize("account1, pwd1, did, name", parameter)
def test_cloudCapture(account1, pwd1, did, name):
    # 登录并进入云回放页面
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("登录")
    app.go_to_page("首页", account1, pwd1)
    app.go_to_page("云回放", name)

    # 回放抓图
    time.sleep(5)
    app.go_to_page("云回放抓图")

    # 进入相册，微信分享给朋友
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("相册")
    # 判断是否有抓图
    assert app.exists_element(selector="resource-id", value="com.zwcode.p6slite:id/item_album_pic_content")
    # 判断抓图个数是否为2
    assert len(app.driver(resourceId="com.zwcode.p6slite:id/item_album_pic_content")) >= 2

    # 清空相册
    app.go_to_page("清空相册")


# 云录像回放中拖动时间轴播放
@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name", parameter)
def test_cloud_seek(account1, pwd1, did, name):
    # 登录并进入云回放页面
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("登录")
    app.go_to_page("首页", account1, pwd1)
    app.go_to_page("云回放", name)
    timelist = [
        '01:00:00',
        '02:00:00',
        '03:00:00',
        '04:00:00',
        '04:29:45',
        '04:30:15',
        '04:45:00',
        '04:59:30',
        '05:00:10',
        '06:00:00',
        '23:59:00'
    ]

    # 录像定位
    for time_str in timelist:
        time.sleep(3)
        app.go_to_page("拖动时间轴", time_str)
        time.sleep(5)
        app.title['wakeup_time'] = time_str.replace(":", "")
        app.go_to_page("截图")


# 进入云存检查时间轴初始位置
@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name", parameter)
def test_check_timeline_initial_position(account1, pwd1, did, name):
    # 登录并进入云回放页面
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("登录")
    app.go_to_page("首页", account1, pwd1)
    app.go_to_page("云回放", name)

    # 获取时间轴的初始位置
    time.sleep(5)
    time_str = app.driver(resourceId="com.zwcode.p6slite:id/tv_time").get_text()
    timestamp = sum(int(x) * 60 ** i for i, x in enumerate(reversed(time_str.split(':'))))

    # 获取当前日期的0点时间戳
    timestamp_0 = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())

    # 对比当前时间与初始位置
    timestamp_now = int(time.time())

    assert abs((timestamp_now - timestamp_0) - (timestamp + 600)) < 60


@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name", parameter)
def test_check_timeline_initial_position_after_cloud_storage_disabled(account1, pwd1, did, name):
    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account1, pwd1)

    # 关闭云存储
    app.title["checked"] = False
    app.go_to_page("云存储开关", name)
    time.sleep(600)

    # 关闭云存储
    app.title["checked"] = True
    app.go_to_page("云存储开关", name)

    # 登录并进入云回放页面
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("登录")
    app.go_to_page("首页", account1, pwd1)
    app.go_to_page("云回放", name)

    # 获取时间轴的初始位置
    time.sleep(5)
    time_str = app.driver(resourceId="com.zwcode.p6slite:id/tv_time").get_text()
    timestamp = sum(int(x) * 60 ** i for i, x in enumerate(reversed(time_str.split(':'))))

    # 获取当前日期的0点时间戳
    timestamp_0 = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())

    # 对比当前时间与初始位置
    timestamp_now = int(time.time())

    assert abs((timestamp_now - timestamp_0) - (timestamp + 1200)) < 120


# 云录像回放中切换不同日期时间播放
@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name", parameter)
def test_cloud_playback_controller(account1, pwd1, did, name):
    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account1, pwd1)
    app.go_to_page("云回放", name)
    app.go_to_page("日历", name)


_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              _config.get('未开通云存储设备', 'did_2'),
              _config.get('未开通云存储设备', 'name_2'),
              account_config.get('支付宝APP', 'PAYMENT_PASSWORD')
              )]


# 使用支付宝购买云存套餐失败
@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name, payment_password", parameter)
def test_handle_alipay_payment_failure(account1, pwd1, did, name, payment_password):
    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account1, pwd1)
    time.sleep(5)
    app.go_to_page('云服务管理', name)

    # 检查套餐是否已开通
    assert app.exists_element(selector="text", value="未开通")

    # 选择套餐并跳转到支付页面
    app.go_to_page('支付宝购买连续录像')
    time.sleep(10)

    # 支付宝支付失败
    if app.exists_element(selector="text", value="忽略"):
        app.driver(text="忽略").click()

    # 放弃支付
    app.driver(className="android.widget.Button").click()
    app.driver(text="放弃").click()
    time.sleep(5)
    assert app.exists_element(selector="text", value="支付失败，请重新支付")

    # 检查云存储状态
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', account1, pwd1)
    app.go_to_page('云服务管理', name)
    time.sleep(3)

    # 检查云存储套餐是否未开通
    assert app.exists_element(selector="text", value="未开通")


@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name, payment_password", parameter)
def test_handle_alipay_payment_success(account1, pwd1, did, name, payment_password):
    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account1, pwd1)
    time.sleep(5)
    app.go_to_page('云服务管理', name)

    # 检查套餐是否已开通
    assert app.exists_element(selector="text", value="未开通")

    # 选择套餐并跳转到支付页面
    app.go_to_page('支付宝购买连续录像')
    time.sleep(10)

    # 支付宝支付失败
    if app.exists_element(selector="text", value="忽略"):
        app.driver(text="忽略").click()

    # 输入密码
    for num in payment_password:
        app.driver(text=num).click()

    # 检查是否支付成功
    time.sleep(5)
    assert app.exists_element(selector="text", value="支付成功")

    # 检查云存储状态
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', account1, pwd1)
    app.go_to_page('云服务管理', name)
    time.sleep(3)

    # 检查云存储套餐是否已开通
    assert not app.exists_element(selector="text", value="未开通")

    # 检查云存储开关是否已开启
    assert app.driver(resourceId="com.zwcode.p6slite:id/param_switch").info.get('checked')

    # 等待10分钟，检查云存是否上传录像
    time.sleep(600)

    # 云回放截图
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("云回放", name)
    time.sleep(5)
    method_name = inspect.stack()[0].function
    app.title['shootName'] = method_name
    app.go_to_page("截图")


_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              _config.get('未开通云存储设备', 'did_1'),
              _config.get('未开通云存储设备', 'name_1'),
              account_config.get('支付宝APP', 'PAYMENT_PASSWORD')
              )]


@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name, payment_password", parameter)
def test_handle_wechat_payment_failure(account1, pwd1, did, name, payment_password):
    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account1, pwd1)
    time.sleep(5)
    app.go_to_page('云服务管理', name)

    # 检查套餐是否已开通
    assert app.exists_element(selector="text", value="未开通")

    # 选择套餐并跳转到支付页面
    app.go_to_page('微信购买连续录像')
    time.sleep(10)

    # 支付宝支付失败
    if app.exists_element(selector="text", value="忽略"):
        app.driver(text="忽略").click()

    # 输入密码
    # for num in payment_password:
    #     app.driver(text=num).click()

    # 放弃支付
    app.driver(resourceId="com.tencent.mm:id/actionbar_up_indicator_btn").click()
    time.sleep(2)
    app.driver(text="放弃").click()
    time.sleep(5)
    assert app.exists_element(selector="text", value="支付失败，请重新支付")

    # 检查云存储状态
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', account1, pwd1)
    app.go_to_page('云服务管理', name)
    time.sleep(3)

    # 检查云存储套餐是否未开通
    assert app.exists_element(selector="text", value="未开通")


@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name, payment_password", parameter)
def test_handle_wechat_payment_success(account1, pwd1, did, name, payment_password):
    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account1, pwd1)
    time.sleep(5)
    app.go_to_page('云服务管理', name)

    # 检查套餐是否已开通
    assert app.exists_element(selector="text", value="未开通")

    # 选择套餐并跳转到支付页面
    app.go_to_page('微信购买连续录像')
    time.sleep(10)

    # 忽略提示自动化风险
    if app.exists_element(selector="text", value="忽略"):
        app.driver(text="忽略").click()

    if app.exists_element(selector="text", value="立即支付"):
        app.driver(text="立即支付").click()

    # 输入密码
    for num in payment_password:
        app.driver(text=num).click()

    # 检查是否支付成功
    time.sleep(5)
    assert app.exists_element(selector="text", value="支付成功")

    # 检查云存储状态
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', account1, pwd1)
    app.go_to_page('云服务管理', name)
    time.sleep(3)

    # 检查云存储套餐是否已开通
    assert not app.exists_element(selector="text", value="未开通")

    # 检查云存储开关是否已开启
    assert app.driver(resourceId="com.zwcode.p6slite:id/param_switch").info.get('checked')

    # 等待10分钟，查看云存回放
    time.sleep(600)

    # 云回放截图
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("云回放", name)
    time.sleep(5)
    method_name = inspect.stack()[0].function
    app.title['shootName'] = method_name
    app.go_to_page("截图")


_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              _config.get('云存储设备', 'did'),
              _config.get('云存储设备', 'name')
              )
             ]


@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name", parameter)
def test_cloud_storage_button_with_active_subscription(account1, pwd1, did, name):
    """
    测试设备已开通未过期的情况下，点击APP首页云存储按钮的功能。
    """
    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 0.5
    app.go_to_page('登录')
    app.go_to_page('首页', account1, pwd1)
    time.sleep(5)
    app.go_to_page('云存储', name)
    time.sleep(5)

    # 检查是否跳转到云存储购买页面
    assert app.exists_element(selector="text", value="连续录像")
    assert app.exists_element(selector="text", value="事件录像")


_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              _config.get('未开通云存储设备', 'did_3'),
              _config.get('未开通云存储设备', 'name_3')
              )]


@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name", parameter)
def test_cloud_storage_button_with_inactive_subscription(account1, pwd1, did, name):
    """
    测试设备未开通云存储服务的情况下，点击APP首页云存储按钮的功能。
    """
    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 0.4
    app.go_to_page('登录')
    app.go_to_page('首页', account1, pwd1)
    time.sleep(5)
    app.go_to_page('云存储', name)
    time.sleep(5)

    # 检查是否跳转到云存储购买页面
    assert app.exists_element(selector="text", value="云端存储")
    assert app.exists_element(selector="text", value="无限空间")
    assert app.exists_element(selector="text", value="数据加密")
    assert app.exists_element(selector="text", value="报警录像")
    assert app.exists_element(selector="text", value="离线可看")
    assert app.exists_element(selector="text", value="一键下载")


_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              _config.get('云存储过期设备', 'did_1'),
              _config.get('云存储过期设备', 'name_1')
              )]


@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name", parameter)
def test_handle_expired_cloud_storage(account1, pwd1, did, name):
    """
    测试设备云存已过期的情况下，点击APP首页云存储按钮的功能。
    """

    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 0.5
    app.go_to_page('登录')
    app.go_to_page('首页', account1, pwd1)
    time.sleep(5)
    app.go_to_page('云存储', name)
    time.sleep(5)

    # 检查是否跳转到云存储购买页面
    assert app.exists_element(selector="text", value="连续录像")
    assert app.exists_element(selector="text", value="事件录像")


_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              _config.get('云存储过期设备', 'did_1'),
              _config.get('云存储过期设备', 'name_1'),
              account_config.get('支付宝APP', 'PAYMENT_PASSWORD')
              )]


@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name, payment_password", parameter)
def test_renew_expired_package(account1, pwd1, did, name, payment_password):
    """
    测试设备云存已过期的情况下，再次开通云存储套餐
    """

    # 前置条件
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 0.5
    app.go_to_page('登录')
    app.go_to_page('首页', account1, pwd1)
    time.sleep(5)
    app.go_to_page('云服务管理', name)
    time.sleep(5)
    app.go_to_page('套餐续费')
    # 选择套餐并跳转到支付页面
    app.go_to_page('微信购买连续录像')
    time.sleep(10)

    # 忽略提示自动化风险
    if app.exists_element(selector="text", value="忽略"):
        app.driver(text="忽略").click()

    if app.exists_element(selector="text", value="立即支付"):
        app.driver(text="立即支付").click()

    # 输入密码
    for num in payment_password:
        app.driver(text=num).click()

    # 检查是否支付成功
    time.sleep(5)
    assert app.exists_element(selector="text", value="支付成功")

    # 检查云存储状态
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('首页', account1, pwd1)
    app.go_to_page('云服务管理', name)
    time.sleep(3)

    # 检查云存储套餐是否已开通
    assert not app.exists_element(selector="text", value="未开通")

    # 检查云存储开关是否已开启
    assert app.driver(resourceId="com.zwcode.p6slite:id/param_switch").info.get('checked')

    # 等待10分钟，查看云存回放
    time.sleep(600)

    # 云回放截图
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("云回放", name)
    time.sleep(5)
    method_name = inspect.stack()[0].function
    app.title['shootName'] = method_name
    app.go_to_page("截图")


_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              _config.get('云存储设备', 'did'),
              _config.get('云存储设备', 'name')
              )
             ]


@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name", parameter)
def test_change_playback_time_seek_to_recorded_segment(account1, pwd1, did, name):
    # 获取当前日期
    current_date = datetime.now()
    # 计算前一天的日期
    previous_date = current_date - timedelta(days=1)
    # 将前一天的日期格式化为字符串
    formatted_previous_date = previous_date.strftime("%Y-%m-%d ") + "12:00:00"
    print("formatted_previous_date", formatted_previous_date)

    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 0.5
    # app.go_to_page('登录')
    app.go_to_page('首页', account1, pwd1)
    time.sleep(5)
    app.go_to_page("选择日期", name, formatted_previous_date)
    app.go_to_page("选择时间", formatted_previous_date)
    app.go_to_page("云回放")

    # 检查跳转的日期和时间是否正确
    time.sleep(6)
    assert app.driver(resourceId="com.zwcode.p6slite:id/tv_day").get_text() == previous_date.strftime("%Y-%m-%d")
    time_str = app.driver(resourceId="com.zwcode.p6slite:id/tv_time").get_text()
    timestamp1 = sum(int(x) * 60 ** i for i, x in enumerate(reversed(time_str.split(':'))))
    timestamp2 = sum(int(x) * 60 ** i for i, x in enumerate(reversed("12:00:00".split(':'))))
    assert abs(timestamp1 - timestamp2) < 8


@pytest.mark.repeat(1)
@pytest.mark.parametrize("account1, pwd1, did, name", parameter)
def test_change_playback_time_seek_to_no_recording(account1, pwd1, did, name):
    # 获取当前日期
    current_date = datetime.now()
    # 计算前一天的日期
    previous_date = current_date - timedelta(days=8)
    # 将前一天的日期格式化为字符串
    formatted_previous_date = previous_date.strftime("%Y-%m-%d ") + "12:00:00"

    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 0.5
    # app.go_to_page('登录')
    app.go_to_page('首页', account1, pwd1)
    time.sleep(5)
    app.go_to_page("选择日期", name, formatted_previous_date)

    # 截图人工检查弹窗
    time.sleep(1)
    app.save_screenshotV1()
