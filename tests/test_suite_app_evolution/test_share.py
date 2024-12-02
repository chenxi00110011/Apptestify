import time
import pytest
import uiautomator2_extended
from router_config import modify_wifi, read_config, router_management, get_sections
from device_reset import reset

"""
========= 6 passed, 84 deselected, 31 warnings in 1551.16s (0:25:51) ==========
"""

_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [
    # 国内手机账户转让设备
    (account_config.get('睿博士正式服账号', '中国手机账户_1'),
     account_config.get('睿博士正式服账号', '中国手机密码_1'),
     _config.get('设备分享', 'did_1'),
     _config.get('设备分享', 'name_1'),
     account_config.get('睿博士正式服账号', '中国邮箱账号_1'),
     account_config.get('睿博士正式服账号', '中国邮箱密码_1'),
     account_config.get('睿博士正式服账号', '中国区号')

     ),
    # 国内邮箱账户转让设备
    (account_config.get('睿博士正式服账号', '中国邮箱账号_1'),
     account_config.get('睿博士正式服账号', '中国邮箱密码_1'),
     _config.get('设备分享', 'did_1'),
     _config.get('设备分享', 'name_1'),
     account_config.get('睿博士正式服账号', '中国手机账户_1'),
     account_config.get('睿博士正式服账号', '中国手机密码_1'),
     account_config.get('睿博士正式服账号', '中国区号')
     ),
    # 国际手机账户转让设备
    (account_config.get('睿博士正式服账号', '泰国手机账户_1'),
     account_config.get('睿博士正式服账号', '泰国手机密码_1'),
     _config.get('设备分享', 'did_1'),
     _config.get('设备分享', 'name_1'),
     account_config.get('睿博士正式服账号', '国际邮箱账户_1'),
     account_config.get('睿博士正式服账号', '国际邮箱密码_1'),
     account_config.get('睿博士正式服账号', '中国区号')
     ),
    # 国际邮箱账户转让设备
    (account_config.get('睿博士正式服账号', '国际邮箱账户_1'),
     account_config.get('睿博士正式服账号', '国际邮箱密码_1'),
     _config.get('设备分享', 'did_1'),
     _config.get('设备分享', 'name_1'),
     account_config.get('睿博士正式服账号', '泰国手机账户_1'),
     account_config.get('睿博士正式服账号', '泰国手机密码_1'),
     account_config.get('睿博士正式服账号', '中国区号')
     ),
    # 美服手机账户转让设备
    (account_config.get('睿博士正式服账号', '美服手机账户_1'),
     account_config.get('睿博士正式服账号', '美服手机密码_1'),
     _config.get('设备分享', 'did_1'),
     _config.get('设备分享', 'name_1'),
     account_config.get('睿博士正式服账号', '美服邮箱账户_1'),
     account_config.get('睿博士正式服账号', '美服邮箱密码_1'),
     account_config.get('睿博士正式服账号', '中国区号')
     ),
    # 美服邮箱账户转让设备
    (account_config.get('睿博士正式服账号', '美服邮箱账户_1'),
     account_config.get('睿博士正式服账号', '美服邮箱密码_1'),
     _config.get('设备分享', 'did_1'),
     _config.get('设备分享', 'name_1'),
     account_config.get('睿博士正式服账号', '美服手机账户_1'),
     account_config.get('睿博士正式服账号', '美服手机密码_1'),
     account_config.get('睿博士正式服账号', '中国区号')
     ),
    # 欧服邮箱账户转让设备
    (account_config.get('睿博士正式服账号', '欧服邮箱账户_1'),
     account_config.get('睿博士正式服账号', '欧服邮箱密码_1'),
     _config.get('设备分享', 'did_1'),
     _config.get('设备分享', 'name_1'),
     account_config.get('睿博士正式服账号', '欧服邮箱账户_2'),
     account_config.get('睿博士正式服账号', '欧服邮箱密码_2'),
     account_config.get('睿博士正式服账号', '中国区号')
     )
]


@pytest.mark.repeat(1)
@pytest.mark.case_name("国内国际，手机账户邮箱账户，转让设备")
@pytest.mark.share_test
@pytest.mark.parametrize("account, pwd, did, name, share_account, share_pwd, areaCode", parameter)
def test_handoverDevice(account, pwd, did, name, share_account, share_pwd, areaCode):
    # 设备复位
    reset(did)
    time.sleep(30)

    # 添加设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account, pwd)
    app.go_to_page('输入WiFi网络', did)
    time.sleep(5)
    app.go_to_page('设备添加成功', 'Ruision-work-CS2.4', 'ruision2024@cs')
    assert app.exists_element(selector='text', value='设备添加成功')

    # 转让设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('首页')
    app.go_to_page('转让设备', name, '分享管理', share_account)

    # 收受设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', share_account, share_pwd)
    app.go_to_page('接受')
    time.sleep(5)
    assert app.exists_element(selector='text', value=name)


_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试邮箱账号', 'account'),
              account_config.get('睿博士测试邮箱账号', 'pwd'),
              account_config.get('睿博士测试手机备用账号', 'account'),
              account_config.get('睿博士测试手机备用账号', 'pwd'),
              _config.get('设备分享', 'did_1'),
              _config.get('设备分享', 'name_1')
              ),
             (account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              account_config.get('睿博士测试手机备用账号', 'account'),
              account_config.get('睿博士测试手机备用账号', 'pwd'),
              _config.get('设备分享', 'did_1'),
              _config.get('设备分享', 'name_1')
              ),
             ]


@pytest.mark.repeat(1)
@pytest.mark.case_name("手机账户输入账户分享设备,邮箱账户输入账户分享设备")
@pytest.mark.share
@pytest.mark.parametrize("account1, pwd1, account2, pwd2, did, name", parameter)
def test_account_sharing(account1, pwd1, account2, pwd2, did, name):
    # 设备复位
    reset(did)
    time.sleep(30)

    # 添加设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("登录")
    app.go_to_page('首页', account1, pwd1)
    app.go_to_page('输入WiFi网络', did)
    time.sleep(5)
    app.go_to_page('设备添加成功', 'Ruision-work-CS2.4', 'ruision2024@cs')
    assert app.exists_element(selector='text', value='设备添加成功')

    # 分享设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('首页', account1, pwd1)
    app.go_to_page('分享给账号', name, '分享管理', account2)

    # 收受设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account2, pwd2)
    app.go_to_page('接受分享')
    time.sleep(3)
    assert app.exists_element(selector='text', value=name)


@pytest.mark.repeat(1)
@pytest.mark.case_name("账户分享二维码")
@pytest.mark.share
@pytest.mark.parametrize("account1, pwd1, account2, pwd2, did, name", parameter)
def test_qr_sharing(account1, pwd1, account2, pwd2, did, name):
    # 设备复位
    reset(did)
    time.sleep(30)

    # 添加设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("登录")
    app.go_to_page('首页', account1, pwd1)
    app.go_to_page('输入WiFi网络', did)
    time.sleep(5)
    app.go_to_page('设备添加成功', 'Ruision-work-CS2.4', 'ruision2024@cs')
    assert app.exists_element(selector='text', value='设备添加成功')

    # 分享设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('首页', account1, pwd1)
    app.go_to_page('二维码', name, '分享管理')

    # 扫描分享二维码
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page('登录')
    app.go_to_page('首页', account2, pwd2)
    app.go_to_page('扫一扫')
    app.go_to_page('等待添加')
    time.sleep(3)
    app.driver(text="去连接").click()

    # 检查是否已成功分享
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    assert app.exists_element(selector='text', value=name)


_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [(account_config.get('睿博士测试手机账号', 'account'),
              account_config.get('睿博士测试手机账号', 'pwd'),
              account_config.get('睿博士测试手机备用账号', 'account'),
              account_config.get('睿博士测试手机备用账号', 'pwd'),
              _config.get('设备分享', 'did_1'),
              _config.get('设备分享', 'name_1')
              ),
             # (account_config.get('睿博士测试邮箱账号', 'account'),
             #  account_config.get('睿博士测试邮箱账号', 'pwd'),
             #  account_config.get('睿博士测试手机备用账号', 'account'),
             #  account_config.get('睿博士测试手机备用账号', 'pwd'),
             #  _config.get('设备分享', 'did'),
             #  _config.get('设备分享', 'name')
             #  )
             ]


@pytest.mark.repeat(1)
@pytest.mark.case_name("账户使用微信分享设备")
@pytest.mark.share
@pytest.mark.parametrize("account1, pwd1, account2, pwd2, did, name", parameter)
def test_WeChat_sharing(account1, pwd1, account2, pwd2, did, name):
    # 设备复位
    reset(did)
    time.sleep(30)

    # 添加设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("登录")
    app.go_to_page('首页', account1, pwd1)
    app.go_to_page('输入WiFi网络', did)
    time.sleep(5)
    app.go_to_page('设备添加成功', 'Ruision-work-CS2.4', 'ruision2024@cs')
    assert app.exists_element(selector='text', value='设备添加成功')

    # 微信分享设备
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('首页', account1, pwd1)
    app.go_to_page('微信分享', name, '分享管理')
    assert app.exists_element(selector="text", value="来自睿博士的分享")

    # 复制分享链接
    app.driver(text="来自睿博士的分享").click()
    time.sleep(5)
    app.driver.click(538, 604)
    time.sleep(1)
    app.driver.click(538, 1350)
    time.sleep(1)
    app.driver.click(538, 1515)
    time.sleep(1)
    app.driver.click(57, 162)
    time.sleep(1)

    # 清空聊天记录
    app.driver(resourceId="com.tencent.mm:id/coz").click()
    app.driver(text="清空聊天记录").click()
    app.driver(text="清空").click()

    # 添加分享
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.go_to_page("登录")
    app.go_to_page('首页', account2, pwd2)
    time.sleep(5)
    app.driver(text="去连接").click()
    time.sleep(5)
    assert app.exists_element(selector="text", value="成功接受分享")
