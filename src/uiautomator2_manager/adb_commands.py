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

    # 重启手机
    REBOOT = "reboot"
    # ... 可以添加更多的ADB指令常量

    # 点击屏幕
    TAP = "shell input tap 100 200"

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


if __name__ == "__main__":
    from config_module import get_config
    # AdbManager().download_file('H675FIS8JJU8AMWW', '../../data/test.apk', rui.APK_DIR)
    # AdbManager().uninstall_app('H675FIS8JJU8AMWW', rui.APP_PACKAGE_NAME)
    # AdbManager().install_app('H675FIS8JJU8AMWW', '../../data/test.apk')
    AdbManager.download_file(
        deviceID='H675FIS8JJU8AMWW',
        local_path=os.path.join(get_config('睿博士').QR_DIR, 'v1.png'),
        remote_path=get_config('睿博士').MOBILE_SCREEN_CAPTUREA
    )


