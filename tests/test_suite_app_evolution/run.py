import os
import time

for i in range(1):
    os.system('pytest -vs -k test_get_event')
    # os.system('pytest -vs -k test_logout')
    # os.system('pytest -vs -k test_register')


