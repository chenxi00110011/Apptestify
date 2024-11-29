import os

for i in range(1):
    os.system('pytest --tb=short --color=yes -m cloud')
    # os.system('pytest -vs -m message')

    # 生成allure报告
    os.system('allure generate ./allure-results -o ./allure-report --clean')