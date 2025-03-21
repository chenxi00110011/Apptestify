import threading
import time
from uiautomator2_manager.adb_commands import AdbManager
from uiautomator2_manager.config_module import get_config
from uiautomator2 import connect


def test_uninstall_and_reinstall():
    # 卸载睿博士app
    AdbManager().uninstall_app('H675FIS8JJU8AMWW', get_config('睿博士').APP_PACKAGE_NAME)

    time.sleep(10)
    # 创建两个线程
    install_thread = threading.Thread(target=AdbManager().install_app, args=('H675FIS8JJU8AMWW',
                                                                         get_config('睿博士').APK_FILE_PATH))
    click_thread = threading.Thread(target=connect('H675FIS8JJU8AMWW')(text='继续安装').click())

    # 启动线程
    install_thread.start()
    time.sleep(10)
    click_thread.start()

    # 等待线程完成
    install_thread.join()
    click_thread.join()

