import time

import requests
import xmltodict
import logging as log
import xrs_time
from my_decorator import exception_handler, write_to_file
from arp_scan import get_ip

log.basicConfig(filename=f'C:\\Users\\Administrator\\Desktop\\logs\\{xrs_time.today()}.log', level=log.INFO)

payload = "telnetd_enable"
headers = {
    'Content-Type': 'XXXX',
    'Accept': 'XXXX',
    'Authorization': 'Basic YWRtaW46',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
}

__dict_url = {
    '打开telnet服务': '/System/DeviceCustomFunction',
    '设备信息': '/System/DeviceInfo',
    '移动运营商信息': '/CM/1/AuthInfo',
    '设备重启': '/System/Reboot',
    '恢复出厂': '/System/FactoryDefaultV2',
    '设备能力': '/System/DeviceCap'
}


@exception_handler
def open_telnet(ip):
    url = ' http://' + ip + __dict_url['打开telnet服务']
    # print(url)
    response = requests.request("PUT", url, headers=headers, data=payload)
    log.info(response.text)


def get_cmei(ip):
    url = f"http://{ip}{__dict_url['移动运营商信息']}"
    r = requests.get(url)
    log.info(r.text)
    return r.text


def set_cmei(ip, _data):
    url = f"http://{ip}{__dict_url['移动运营商信息']}"
    r = requests.put(url, data=_data)
    log.info(r.status_code)
    return r.status_code


def system_reboot(ip):
    url = ' http://' + ip + __dict_url['设备重启']
    response = requests.request("PUT", url, headers=headers, data=payload)
    log.info(response.text)


@exception_handler
def system_factoryDefault(ip=None, mac=None):
    if ip is None:
        ip = get_ip(mac)
    url = ' http://' + ip + __dict_url['恢复出厂']
    response = requests.request("PUT", url, headers=headers, data=payload)
    log.info(response.text)
    time.sleep(15)


def getDeviceTypeName(ip):
    url = ' http://' + ip + __dict_url['设备信息']
    response = requests.get(url, headers=headers, data=payload).text
    d = xmltodict.parse(response)
    result = d['DeviceInfo']['DeviceTypeName']
    log.info(result)
    return result


def getDeviceVersion(ip):
    """
    获取设备信息
    :param ip:
    :return:
    """
    url = ' http://' + ip + __dict_url['设备信息']
    response = requests.get(url, headers=headers, data=payload).text
    d = xmltodict.parse(response)
    result = d['DeviceInfo']
    log.info(result)
    return result


@write_to_file(
    f"C:\\Users\\Administrator\\PycharmProjects\\AutoDriver_UIA2\\venv\\data\\{xrs_time.current_time(mod='log')}_deviceInfo")
def getDeviceInfo(ip):
    """
        获取设备信息
        :param ip:
        :return:
        """
    url = ' http://' + ip + __dict_url['设备信息']
    response = requests.get(url, headers=headers, data=payload).text
    # result = xmltodict.parse(response)
    return response


@write_to_file(
    f"C:\\Users\\Administrator\\PycharmProjects\\AutoDriver_UIA2\\venv\\data\\{xrs_time.current_time(mod='log')}_deviceCap")
def getDeviceCap(ip):
    """
        获取设备信息
        :param ip:
        :return:
        """
    url = ' http://' + ip + __dict_url['设备能力']
    response = requests.get(url, headers=headers, data=payload).text
    # result = xmltodict.parse(response)
    return response


def all_open_telnet(ip_list: list):
    for ip in ip_list:
        open_telnet(ip)


if __name__ == '__main__':
    ip_list = ['192.168.123.145']
    for ip in ip_list:
        open_telnet(ip)

