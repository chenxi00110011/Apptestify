# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
import subprocess
from config_module import ConfigManagerRUIBOSHI  as rui


class AdbManager:
    # ADB指令常量
    LIST_DEVICES = "devices"
    ADB_INSTALL_APP = "install {}"
    ADB_SET_INPUT_METHOD = "shell ime set {}"
    LIGHT_UP_SCREEN = 'shell input keyevent 224'
    UNLOCK_SCREEN = 'shell input swipe 300 1000 300 500'
    SCREEN_SHOOT = f'shell screencap -p {rui.MOBILE_SCREEN_CAPTUREA}screenshot.png'

    # ... 可以添加更多的ADB指令常量

    @staticmethod
    def execute_command(deviceID, command):
        """执行ADB命令并返回输出"""
        command = f'adb -s {deviceID}' + ' '+command
        print(command)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise Exception(f"ADB命令执行失败: {stderr.decode()}")
        return stdout.decode()

    @staticmethod
    def install_app(apk_path):
        """安装应用"""
        command = AdbManager.ADB_INSTALL_APP.format(apk_path)
        return AdbManager.execute_command(command)

    @staticmethod
    def set_default_input_method(deviceID, input_method_package):
        """设置默认输入法"""
        command = AdbManager.ADB_SET_INPUT_METHOD.format(input_method_package)
        return AdbManager.execute_command(deviceID, command)


if __name__ == "__main__":
    AdbManager().set_default_input_method('io.appium.settings/.UnicodeIME')
