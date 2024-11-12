import pytest
from adb_commands import AdbManager


# 定义 fixture 来连接 Wi-Fi
@pytest.fixture(scope="function", autouse=True)
def connect_to_wifi():
    # 手机连接Wi-Fi
    AdbManager.connect_network('H675FIS8JJU8AMWW', 'Ruision-work-CS5', 'ruision2024@cs')
