# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
import time

import requests
import xmltodict
from device_endpoints import DevEndpoints
from my_decorator import exception_handler


class DeviceAPIManager(DevEndpoints):

    @exception_handler
    def put_data_to_endpoint(self, endpoints):
        url = self.get_full_url(endpoints)
        print(url)
        response = requests.request("PUT", url, headers=self.HEADERS, data=self.PAYLOAD)  # 假设格式化SD卡使用PUT方法
        response.raise_for_status()  # 如果请求失败，这会抛出HTTPError异常
        print(response.status_code)
        return response

    # @exception_handler
    def get_data_from_endpoint(self, endpoints, params=None):
        url = self.get_full_url(endpoints)
        response = requests.request("GET", url, headers=self.HEADERS, params=params)
        print(xmltodict.parse(response.text))
        print('_' * 100)
        return xmltodict.parse(response.text)

    # 格式化SD卡
    def format_sdcard(self):
        return self.put_data_to_endpoint(self.SD_CARD_FORMAT)

    # 打开设备的telnet服务
    def open_telnet(self):
        return self.put_data_to_endpoint(self.OPEN_TELENT)

    # 获取SD卡信息
    def get_sdcard_info(self):
        return self.get_data_from_endpoint(self.SD_INFO)

    # 重启设备
    def dev_reboot(self):
        return self.put_data_to_endpoint(self.REBOOT)

    # 恢复出厂
    def reset_to_factory_settings(self):
        return self.put_data_to_endpoint(self.FACTORY_DEFAULT)

    # 反向打包
    def device_reverse_packet(self):
        return self.put_data_to_endpoint(self.DEVICE_REVERSE_PACKET)

    # 获取时间信息
    def get_time_info(self):
        return self.get_data_from_endpoint(self.TIME_INFO)

    # 设置IR_CUT值
    def set_ir_cut_filter_config(self):
        return self.put_data_to_endpoint(self.IR_CUT_FILTER)



if __name__ == '__main__':
    endpoints = DeviceAPIManager('192.168.156.137')
    endpoints.open_telnet()
    # endpoints.device_reverse_packet()
    # endpoints.get_sdcard_info()
    # endpoints.get_time_info()

    # # 设备重启
    # endpoints.dev_reboot()
    # time.sleep(45)

    # 获取SD卡信息
    # res = endpoints.get_sdcard_info()
    # print(res['DiskList']['Disk']['DiskStorageAttribute'])

    # # 格式化SD卡
    # endpoints.format_sdcard()
    # time.sleep(30)
    #
    # # 获取SD卡信息
    # res = endpoints.get_sdcard_info()
    # print(res['DiskList']['Disk']['DiskStorageAttribute'])
