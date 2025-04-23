# -*- coding: utf-8 -*-
"""
Author: chen xi
Date: 2025/1/14 上午9:18
File: test_aov_wakeup.py
"""
import time
import pytest
import uiautomator2_extended
from datetime import datetime

# 需要唤醒的设备，填写APP上的设备名称
parameter = [
	# '000116',
	'000055',
	'000124',
	# '000084',
	# '000083',
	# '000024',
	# '000025',
	# '000018',
	# '000028',
	# '000039',
]

# 预览时长，单位秒
timePreview = 30


@pytest.mark.aov_v1
@pytest.mark.case_name("设备唤醒")
@pytest.mark.parametrize("name", parameter)
@pytest.mark.repeat(1)
def test_aov_wakeup(name):
	# 启动APP
	app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
	time.sleep(20)
	app.go_to_page("首页", '2389958090@qq.com', 'yu123456')
	
	app.WAIT_TIME = 0
	app.go_to_page('直播', name)
	
	# 获取当前时间并格式化为字符串
	current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
	start_time = time.time()
	count = 0
	while not app.exists_element(selector="text", value="画质") and count < 30:
		count += 1
		time.sleep(0.5)
	end_time = time.time()
	
	# 要写入的内容
	content = "{:.2f}".format(end_time - start_time)
	# 写入文件
	with open('example.txt', 'a') as file:
		file.write(f"[{current_time}]\t{name}\t{content}\n")
	
	time.sleep(timePreview)
	app.app_stop_()
	time.sleep(10)
