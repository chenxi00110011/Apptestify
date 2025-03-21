# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
import os
import subprocess
from config_module import ConfigManagerRUIBOSHI as rui


class AdbManager:
    # 展示手机连接状态
    LIST_DEVICES = "devices"

    # 安装app，注意apk路径为电脑存放路径
    ADB_INSTALL_APP = "install {}"

    # 卸载app
    ADB_UNINSTALL_APP = "uninstall {}"

    # 设置输入法
    ADB_SET_INPUT_METHOD = "shell ime set {}"

    # 屏幕点亮
    LIGHT_UP_SCREEN = 'shell input keyevent 224'

    # 解锁屏幕
    UNLOCK_SCREEN = 'shell input swipe 300 1000 300 500'

    # 截图
    SCREEN_SHOOT = f'shell screencap -p {rui.MOBILE_SCREEN_CAPTUREA}screenshot.png'

    # 从电脑下载文件到手机
    DOWNLOAD_FILE = "push {} {}"

    # 从手机下载文件到电脑
    PULL_FILE = "pull {} {}"

    # 重启手机
    REBOOT = "reboot"
    # ... 可以添加更多的ADB指令常量

    # 点击屏幕
    TAP = "shell input tap 100 200"

    # 手机连接Wi-Fi
    CONNECT_NETWORK = "shell cmd wifi connect-network {} wpa2 {}"

    @staticmethod
    def execute_command(deviceID: str, command: str):
        """执行ADB命令并返回输出"""
        command = f'adb -s {deviceID}' + ' ' + command
        print(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise Exception(f"ADB命令执行失败: {stderr.decode()}")
        return stdout.decode()

    @staticmethod
    def install_app(deviceID: str, apk_path: str):
        """安装应用"""
        command = AdbManager.ADB_INSTALL_APP.format(apk_path)
        return AdbManager.execute_command(deviceID, command)

    @staticmethod
    def uninstall_app(deviceID: str, package_name: str):
        """安装应用"""
        command = AdbManager.ADB_UNINSTALL_APP.format(package_name)
        return AdbManager.execute_command(deviceID, command)

    @staticmethod
    def set_default_input_method(deviceID: str, input_method_package: str):
        """设置默认输入法"""
        command = AdbManager.ADB_SET_INPUT_METHOD.format(input_method_package)
        return AdbManager.execute_command(deviceID, command)

    @staticmethod
    def download_file(deviceID: str, local_path: str, remote_path: str):
        """下载文件到手机"""
        command = AdbManager.DOWNLOAD_FILE.format(local_path, remote_path)
        return AdbManager.execute_command(deviceID, command)

    @staticmethod
    def connect_network(deviceID: str, ssid: str, pwd: str):
        """下载文件到手机"""
        command = AdbManager.CONNECT_NETWORK.format(ssid, pwd)
        return AdbManager.execute_command(deviceID, command)

    @staticmethod
    def pull_file(deviceID: str, down_file, des_path):
        """下载文件到手机"""
        command = AdbManager.PULL_FILE.format(down_file, des_path)
        return AdbManager.execute_command(deviceID, command)

    @staticmethod
    def clear_all_background_apps():
        try:
            # 检查设备是否连接
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            if "device" not in result.stdout:
                print("No device found. Please connect your Android device and enable USB debugging.")
                return

            # 按下最近任务键
            subprocess.run(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_APP_SWITCH'])

            # 模拟滑动手势清除所有后台应用
            # 这里假设屏幕分辨率为 1˜080x1920，你可以根据实际情况调整
            for _ in range(5):  # 尝试滑动多次，确保清除所有应用
                subprocess.run(['adb', 'shell', 'input', 'swipe', '500', '1500', '500', '500', '100'])

            print("All background apps cleared.")

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":

    AdbManager.pull_file('H675FIS8JJU8AMWW', "/sdcard/Pictures/P6SLite/screenshot", r'C:\Users\Administrator\Desktop\video\test')