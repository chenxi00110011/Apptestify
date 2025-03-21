import os
import time

# for i in range(200):
#     # os.system('pytest --tb=short --color=yes -m bind_test')
#     os.system('pytest -vs -m gc_qr')
#
#     # 生成allure报告
#     # os.system('allure generate ./allure-results -o ./allure-report --clean')


for i in range(999999):
    # os.system('pytest --tb=short --color=yes -m bind_test')
    os.system('pytest -vs -m aov_v1')

    # 生成allure报告
    # os.system('allure generate ./allure-results -o ./allure-report --clean')

