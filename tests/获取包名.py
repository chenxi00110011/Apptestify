# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
from uiautomator2 import connect

# 连接到你的设备，确保你的设备已经通过USB调试模式连接到电脑
d = connect('H675FIS8JJU8AMWW')

# 获取当前包名
current_package = d.app_current()['package']
print("Current package name:", current_package)
current_info = d.app_current()
current_activity = current_info['activity']
print("Current activity name:", current_activity)