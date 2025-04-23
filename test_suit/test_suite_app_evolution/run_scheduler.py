# -*- coding: utf-8 -*-
"""
Author: chen xi
Date: 2025/3/21 上午10:40
File: run_scheduler.py
"""

import os
import schedule
import time


def run_pytest(times, mark):
	for i in range(times):
		os.system(f'pytest -vs -m {mark}')
		# 如果需要生成allure报告，请取消以下注释
		# os.system('allure generate ./allure-results -o ./allure-report --clean')
		# 这里根据需要调整每次运行后的等待时间，避免过快连续执行
		time.sleep(300)  # 可以根据实际情况调整或移除等待时间


# 安排任务
run_pytest(40, 'aov_v1')
schedule.every().day.at("08:00").do(run_pytest, times=60, mark='aov_v1')
schedule.every().day.at("23:00").do(run_pytest, times=40, mark='aov_v1')

print("等待开始执行...")
while True:
	schedule.run_pending()
	time.sleep(1)
