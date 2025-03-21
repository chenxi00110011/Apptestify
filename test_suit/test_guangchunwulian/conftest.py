import shutil
import pytest
from datetime import datetime
from adb_commands import AdbManager
import os
import subprocess
import time
import console_ctrl
from adb_commands import AdbManager as adb, AdbManager
from router_config import read_config

config = read_config(r'..\..\config\base.ini')


# 定义 fixture 来连接 Wi-Fi
@pytest.fixture(scope="function", autouse=True)
def connect_to_wifi():
    # # 点亮屏幕和解锁
    adb.execute_command('H675FIS8JJU8AMWW', adb.LIGHT_UP_SCREEN)
    adb.execute_command('H675FIS8JJU8AMWW', adb.UNLOCK_SCREEN)
    # 手机连接Wi-Fi
    AdbManager.connect_network('H675FIS8JJU8AMWW', config.get('测试Wi-Fi', 'ssid'),
                               config.get('测试Wi-Fi', 'wifi_password'))
    AdbManager.clear_all_background_apps()


# 全局变量来存储录像进程
recording_process = None
video_path = ""  # 全局变量来存储视频路径


def start_recording(test_name):
    global recording_process, video_path
    # 获取当前日期并格式化为字符串
    current_date = datetime.now().strftime("%Y%m%d")
    # 定义录像文件的路径
    video_path = f"D:/videos/{current_date}/{test_name}.mp4"
    # 确保视频目录存在
    os.makedirs(os.path.dirname(video_path), exist_ok=True)

    # 启动 scrcpy 录像
    command = [
        "scrcpy",
        "--no-playback",  # 不显示视频窗口
        "--record", video_path,  # 直接录制到指定文件
        "--prefer-text",  # 使用文本模式显示日志信息
        "--stay-awake",  # 保持设备唤醒状态
        "--video-bit-rate=1M",  # 设置最大比特率为 2 Mbps
        "--no-audio"  # 禁用音频采集
    ]

    # 启动录制进程
    recording_process = subprocess.Popen(command,
                                         shell=True,
                                         creationflags=subprocess.CREATE_NEW_CONSOLE,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)


# 停止录屏函数
def stop_recording():
    global recording_process
    if recording_process and recording_process.poll() is None:
        console_ctrl.send_ctrl_c(recording_process.pid)


def rename_video_file(old_path, result):
    new_path = old_path.replace('.mp4', f'_{result}.mp4')
    try:
        os.rename(old_path, new_path)
        print(f"成功将 {old_path} 重命名为 {new_path}")
    except FileNotFoundError:
        print(f"错误: 文件 {old_path} 未找到")
    except Exception as e:
        print(f"发生错误: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True, scope="function")
def record_video(request):
    # 获取用例名称（假设在测试用例中通过标记传递）
    marker = request.node.get_closest_marker("case_name")
    if marker:
        case_name = marker.args[0]
    else:
        case_name = request.node.name  # 使用测试函数名作为默认case_name

    # 获取当前时间并格式化为字符串（仅时分秒）
    timestamp = datetime.now().strftime("%H%M%S")
    case_name_with_timestamp = f"{timestamp}_{case_name}"

    # 执行用例前开始录像
    start_recording(case_name_with_timestamp)
    yield
    # 执行用例完成后停止录像
    stop_recording()

    # 获取测试结果
    test_result = "pass" if hasattr(request.node, 'rep_call') and request.node.rep_call.passed else "fail"

    # 重命名录像文件
    rename_video_file(video_path, test_result)


@pytest.fixture(scope="session", autouse=True)
def clean_and_generate_allure_report():
    results_dir = './allure-results'

    # 清理操作：删除目录中的所有文件和子目录，但保留目录本身
    if os.path.exists(results_dir):
        for filename in os.listdir(results_dir):
            file_path = os.path.join(results_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # 删除文件或符号链接
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # 递归删除子目录
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        print(f"Contents of directory {results_dir} have been removed.")
    else:
        print(f"Directory {results_dir} does not exist, nothing to remove.")

    # 创建 allure-results 目录（如果不存在）
    if not os.path.exists(results_dir):
        os.makedirs(results_dir, exist_ok=True)
        print(f"Directory {results_dir} has been created.")

    # 这里是测试函数实际执行的地方
    yield
