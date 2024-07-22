# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
import uiautomator2_extended
from arp_scan import get_ip
from device_api import DeviceAPIManager
import time
from telnet_client import telnet_connect
from xrs_serial import serial_bitstream


def device_reset(ip):
    dev = DeviceAPIManager(ip)
    dev.open_telnet()
    username = "root"
    password = "zviewa5s"
    commands = [
        'rm /usr/local/etc/scode.conf',
        'rm /usr/local/etc/scode_bak.conf',
        'echo -e  "[system]\ndvr=idvr9000\n\n[ERP]\nSCode=@172137253585107989654817-0300000\n\ndvr=idvr9000" >>/usr/local/etc/scode_bak.conf',
        'echo -e  "[system]\ndvr=idvr9000\n\n[ERP]\nSCode=@172137253585107989654817-0300000\n\ndvr=idvr9000" >>/usr/local/etc/scode.conf'
    ]
    for command in commands:
        telnet_connect(ip, username, password, command)
    dev.reset_to_factory_settings()


for i in range(100):
    ip = get_ip("70:3A:2D:A5:CB:71")
    device_reset(ip)
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', "好威智")
    if ip:
        device_reset(ip)
    else:
        serial_bitstream('com38', '断电', 5)
        serial_bitstream('com38', '上电', 1)
    time.sleep(60)
    app.go_to_page("蓝牙搜索设备")
    app.go_to_page("输入WiFi网络", 'did:IOTDDD-074857-ZLYMW')
    app.go_to_page("蓝牙-设备连接中", "ruision_chenxi_2.4", "cx12345678")
    start_time = time.time()
    count = 0
    while not (app.exists_element(selector="text", value="设备添加成功") or
               app.exists_element(selector="text", value="抱歉，设备添加失败")):
        time.sleep(1)
        count += 1
        if count >= 60:
            break
    end_time = time.time()
    app.title['wakeup_time'] = '{:.2f}'.format(end_time - start_time + 10)
    print(f"绑定用时:{end_time - start_time}")
    app.go_to_page("截图")

