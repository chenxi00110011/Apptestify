import time
from uiautomator2_extended import Uiautomator2SophisticatedExecutor


def locationCheck():
    pages = ["登录", "首页", "设备设置", "直播", "我的", "相册", "账号与安全"]
    for pageName in pages:
        app = Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
        time.sleep(15)
        app.go_to_page("首页", "18086409233", "cx123456789")
        app.go_to_page(pageName)
        if app.get_current_page() == pageName:
            print(f"{pageName}页面检测：PASS")
        else:
            print(f"{pageName}页面检测：Faile")

locationCheck()