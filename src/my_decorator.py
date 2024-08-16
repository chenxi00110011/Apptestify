# -*- coding: utf-8 -*-

import logging as log
import os
import re
import threading
import time
from functools import wraps
from pathlib import Path
import schedule
import environment_variable
import ntp_util
import xrs_adb
import xrs_time
import adb_commands
from loguru import logger
from config_module import ConfigManagerRUIBOSHI as rui

logger.add(rui.LOGS_DIR + f"\\{ntp_util.timestamp_to_date()}.log", encoding="utf-8")

desktop_path = Path(os.path.expanduser("~")) / "Desktop"
# print(desktop_path, type(desktop_path))
log_save_path = str(desktop_path) + "\\logs\\"
# print(log_save_path, type(log_save_path))
if not os.path.exists(log_save_path):
    os.mkdir(log_save_path)
log.basicConfig(filename=log_save_path + f"{xrs_time.today()}.log", level=log.INFO)
'''
1、运行花费时间，返回函数或方法的执行时间
2、打印函数的执行时的时间
3、打印函数的返回值
4、保存日志
'''
error_dict = {
    '未找到页面元素': 'selenium.common.exceptions.NoSuchElementException: Message: An element could not be located on the page using the given search parameters.',
    '': ''
}


def create_folder_if_not_exists(folder_path):
    """
    判断文件夹是否存在，如果不存在则创建它。
    参数:
    folder_path (str): 文件夹路径。
    返回:
    None
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def timer(func):
    """打印方法的执行时间"""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = "{:.6f}".format(end_time - start_time)
        logger.info(f"Method [{func.__name__}] took {execution_time} seconds to execute.")
        return result

    return wrapper


def print_current_time(func):
    # 打印函数的执行时间
    def wrapper(*args, **kwargs):
        logger.info(xrs_time.get_current_time(), f"开始执行函数{func.__name__}")
        func(*args, **kwargs)

    return wrapper


def screenshot(shot_path=None):
    """
    截图装饰器，可以传入截图保存路径参数。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            adb = adb_commands.AdbManager()
            temp = func(*args, **kwargs)  # 调用被装饰的函数
            result = temp
            wakeup_time = temp.title['wakeup_time']
            create_folder_if_not_exists(shot_path)
            file_path = shot_path + f"//{result.androidDeviceID}"
            create_folder_if_not_exists(shot_path + f"//{result.androidDeviceID}")
            file_path = file_path + f'//{result.did}'
            create_folder_if_not_exists(file_path)
            file_path = file_path + f'//{ntp_util.timestamp_to_date()}'
            create_folder_if_not_exists(file_path)
            filename = ntp_util.timestamp_to_date(format="%H-%M-%S") + f'-{wakeup_time}' + '.PNG'
            # 执行手机截屏命令
            os.system(adb.execute_command(result.androidDeviceID, adb.SCREEN_SHOOT))
            os.system(
                f'adb -s {result.androidDeviceID} pull {environment_variable.mobile_screen_capture}screenshot.png {file_path}\\{filename}')
            return None  # 返回被装饰函数的返回值

        return wrapper

    return decorator


def print_return(func):
    # 打印函数的返回值
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        logger.info(res)

    return wrapper


def debug(head=None, print_flag=True):
    # 装饰器工厂函数，它接受两个参数：head（前缀）和print_flag（是否打印的标记）
    def decorator(func):
        # 内部装饰器函数，它接受一个函数func作为参数，并返回一个新的函数wrapper
        def wrapper(*args, **kwargs):
            # 调用原始函数func，并将结果存储在变量res中
            res = func(*args, **kwargs)
            # 如果print_flag为True，则打印返回值
            if print_flag:
                # 如果提供了head前缀，则在返回值前面打印它
                print(head, res)
                # 返回函数的原始结果
            return res

            # 返回wrapper函数，它将作为被装饰函数的替代

        return wrapper

        # 返回内部装饰器函数decorator，它将被应用到被装饰的函数上

    return decorator


def print_list_items(func):
    def wrapper(*args, **kwargs):
        # 调用原始函数并获取其返回的列表

        result_list = func(*args, **kwargs)

        # 逐个打印列表中的元素

        for item in result_list:
            logger.info(item)

        # 返回原始函数的结果，以便可以继续使用它

        return result_list

    # 返回wrapper函数，它将作为被装饰函数的替代

    return wrapper


def printer(func):
    # 打印方法的执行时间
    # 打印函数的返回值
    # 打印函数名称
    # 打印当前函数执行时间
    def wrapper(*args, **kwargs):
        logger.info(xrs_time.get_current_time(), f"开始执行函数{func.__name__}")  # 打印开始执行的时间
        start_time = time.time()  # 记录开始执行的时间戳
        res = func(*args, **kwargs)
        end_time = time.time()  # 记录结束执行的时间戳
        execution_time = "{:.6f}".format(end_time - start_time)
        logger.info(f"Method [{func.__name__}] took {execution_time} seconds to execute.")  # 打印执行所需时间
        logger.info(f"函数{func.__name__}执行结果:{res}")  # 打印返回值
        logger.info(f"函数{func.__name__}执行结果类型:{type(res)}")  # 打印返回值
        return res

    return wrapper


def save_log(func):
    # 保存函数的返回值到日志，带时间戳
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        log.info('\t' + xrs_time.get_current_time() + '\n' + res)

    return wrapper


def thread_decorator(func):
    # 实现装饰器开启多线程
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


def timed_executor(t):
    def decorator(func):
        def run_threaded(func, *args, **kwargs):
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()
            return thread

        def wrapper(*args, **kwargs):
            schedule.clear()
            schedule.every().day.at(t).do(run_threaded, func, *args, **kwargs)
            while True:
                schedule.run_pending()

        return wrapper

    return decorator


def exception_handler(func):
    """抛出异常"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception caught: {e}")

    return wrapper


def retry(retries=2, delay=8):
    """
    装饰器：函数执行失败后会尝试多次重试

    :param retries: 重试次数，默认为3次
    :param delay: 重试延迟时间，单位为秒，默认为1秒

    使用示例：

    @retry(retries=5, delay=2)
    def my_function():
        # 进行一些操作
        pass

    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.info(f'{func.__name__} failed with error: {str(e)}')
                    if i <= retries - 1:
                        time.sleep(delay * (i + 1))  # 每次等待时间与异常次数成线性关系
                    else:
                        raise Exception(F"尝试{retries}次重新执行后，仍然运行异常！")
            return None

        return wrapper

    return decorator


def repeat(num_repeats):
    # 装饰器，用于多次执行，且含异常检查
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(num_repeats):
                logger.info(f"{xrs_time.get_current_time()}\tRunning {i + 1}/{num_repeats}...")
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error: {e}")
                    try:
                        xrs_adb.start_app('com.zwcode.p6slite', '.activity.SplashActivity')
                        continue
                    except Exception as e:
                        logger.error(f"Error: {e}")
                        xrs_adb.start_app('com.zwcode.p6slite', '.activity.SplashActivity')
                        continue
                time.sleep(1)

        return wrapper

    return decorator


def schedule_task(interval, unit="every"):
    """
    实现定时任务的装饰器
    提供两种方法：
    方法1：    unit="every" 每间隔interval秒执行1次任务，默认该方法
    方法2：    unit="day"   每天固定时间点interval执行任务
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

            # 使用schedule安排任务

        if unit == "every":
            schedule.every(int(interval)).seconds.do(wrapper)  # 以interval秒循环执行
        elif unit == "day":
            schedule.every().day.at(interval).do(wrapper)  # 每天时间点interval循环执行
        else:
            raise Exception("参数unit错误")

        # 返回一个函数，用于取消任务（如果需要）
        def cancel_job():
            job = next((job for job in schedule.jobs if job.func == wrapper), None)
            if job:
                job.cancel()

        return cancel_job

    return decorator


def write_to_file(file_path):
    """
    把结果写到指定目录
    :param file_path:
    :return:
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(file_path, 'a') as f:
                f.write(str(result) + '\n')
            return result

        return wrapper

    return decorator


# 多线程装饰器
def threading_decorator(func):
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs)

        t.start()

        return t

    return wrapper


def forbidden_method(func):
    def wrapper(*args, **kwargs):
        raise Exception("This method is forbidden to be used.")

    return wrapper


# 定义一个装饰器工厂，它接收一个正则表达式作为参数
def match_pattern_in_list(pattern):
    # 编译正则表达式，以便在装饰器内部多次使用，提高效率
    compiled_pattern = re.compile(pattern)

    # 返回一个真正的装饰器，它接受一个函数作为参数
    def decorator(func):
        # 定义一个包装函数，它将替代原函数的调用
        def wrapper(*args, **kwargs):
            # 调用原始函数，并获取其返回值
            result = func(*args, **kwargs)

            # 检查原始函数的返回值是否为列表
            if isinstance(result, list):
                # 使用列表推导式，遍历列表中的每一个元素
                # 对于每一个元素，使用finditer方法查找所有匹配正则表达式的子串
                # 如果找到匹配，使用match.group()获取匹配的子串，并将其收集到新的列表中
                matched_items = [match.group() for item in result for match in compiled_pattern.finditer(item)]

                # 返回包含所有匹配子串的新列表
                return matched_items
            else:
                # 如果原始函数的返回值不是列表，抛出一个ValueError异常
                raise ValueError("The decorated function must return a list.")

        # 返回包装函数，它将替代原函数
        return wrapper

    # 返回装饰器工厂，等待接收一个函数参数
    return decorator

if __name__ == '__main__':
    logger.info(ntp_util.timestamp_to_date())
