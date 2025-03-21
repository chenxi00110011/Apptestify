import os
import time

for i in range(100):
    # os.system('pytest --tb=short --color=yes -m bind_test')
    os.system('pytest -vs -m gcwl')

    # 生成allure报告
    # os.system('allure generate ./allure-results -o ./allure-report --clean')
