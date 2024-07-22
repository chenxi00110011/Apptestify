import re
import socket
import struct


PORT = 5556

receiveSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建socket
address = ("192.168.123.11", PORT)
receiveSocket.bind(address)  # 绑定ip及端口

device_count = 0
ip_list = []
device_list = []
while device_count < 100:
    # print("等待接收msg")
    message, client = receiveSocket.recvfrom(2147483647)  # 接收数据
    # if client[0] in ip_list:
    #     # print('------------------------')
    #     break

    encodings = ['utf-8', 'gbk', 'latin-1', 'ascii']
    string = message.decode('latin-1')

    regex = r"[a-zA-Z0-9.\-/]+"
    matches = re.findall(regex, string)
    # 输出匹配到的结果
    print(matches)
    output_str = "\n".join(matches)
    print(output_str)
    # print(output_str)
    # print(f'设备IP：{client[0]}')

    ip_list.append(client[0])
    device_list.append(output_str)
    device_count += 1

ip_list = list(set(ip_list))
device_list = list(set(device_list))

print(ip_list)
print(len(ip_list))
for ip in ip_list:
    if ip in device_list:
        print()
# print(f'局域网摄像头数量：{device_count}')
