from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import time
import pytest
import uiautomator2_extended
from router_config import modify_wifi, read_config, router_management, get_sections
from device_reset import reset

# 初始化设备
auto_setup(__file__)

# 连接到 Android 设备
device = connect_device("Android:///")

# 初始化 Poco
poco = AndroidUiautomationPoco(device=device, use_airtest_input=True, screenshot_each_action=False)

# 启动应用
start_app("com.zwcode.p6slite")

# # 通过 Poco 定位和操作控件
# poco("com.example.yourapp:id/button").click()
#
# # 通过图像识别点击某个元素
# touch(Template(r"your_image_path.png", threshold=0.7))
#
# # 更多操作...

# 添加设备
app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
time.sleep(15)