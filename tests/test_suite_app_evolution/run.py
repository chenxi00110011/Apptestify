import os

for i in range(1):
    os.system('pytest -vs -k test_enableCloudSwitch')
    # os.system('pytest --tb=short --color=yes -m message')
