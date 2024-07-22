# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
from arp_scan import get_ip


class DevEndpoints:
    def __init__(self, base_url=None, mac=None):
        if mac:
            self.base_url = "http://" + get_ip(mac)
        elif base_url:
            self.base_url = "http://" + base_url

        # 定义常量端点

    # 打开设备telnet服务
    OPEN_TELENT = '/System/DeviceCustomFunction'

    # 获取设备信息
    DEVICE_INFO = '/System/DeviceInfo'

    # 获取移动运营商固化信息
    CM_AUTH = '/CM/1/AuthInfo'

    # 设备重启
    REBOOT = '/System/Reboot'

    # 恢复出厂
    FACTORY_DEFAULT = '/System/FactoryDefaultV2'

    # 获取设备能力
    DEVICE_CAP = '/System/DeviceCap'

    # 格式化SD卡
    SD_CARD_FORMAT = '/Record/Format/Call'

    # SD卡信息
    SD_INFO = '/Disk'

    # 反向打包
    DEVICE_REVERSE_PACKET = '/System/DeviceReversePacket'

    # 时间信息
    TIME_INFO = '/System/Time'

    # IR_CUT信息
    IR_CUT_FILTER = '/Images/1/IrCutFilter'

    # ... 添加其他常量端点

    PAYLOAD = "telnetd_enable"
    HEADERS = {
        'Content-Type': 'XXXX',
        'Accept': 'XXXX',
        'Authorization': 'Basic YWRtaW46',
        'User-Agent': 'SDK C++ http client'
    }

    def get_full_url(self, endpoint, **kwargs):
        # 格式化端点中的变量部分
        formatted_endpoint = endpoint.format(**kwargs)
        return f"{self.base_url}{formatted_endpoint}"

    # 示例使用


if __name__ == "__main__":
    endpoints = DevEndpoints('http://192.168.123.140')
    # 获取用户列表的完整 URL
    # users_url = endpoints.get_full_url(endpoints.SD_CARD_FORMAT)
    # print(users_url)  # 输出: https://api.example.com/users
