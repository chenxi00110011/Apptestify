import os
import time
from my_decorator import schedule_task
import schedule

if __name__ == '__main__':

    # @schedule_task("20:17", "day")
    # def job():
    #     os.system('pytest -vs -m test_aov_device_binding_success')
    #
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    for i in range(3000):
        os.system('pytest -vs -m aov_core_huawei')