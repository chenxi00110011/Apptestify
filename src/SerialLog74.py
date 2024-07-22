"""
直接安装pyserial库即可，不要安装serial库
"""
import os
import time
import serial
from push_message import countersign, ding_talk_robots, send_dd_news

serial_com = 'COM34'

ser = serial.Serial(serial_com, 115200, timeout=5)
# ser = serial.Serial(serial_com, 1500000, timeout=5)
# print(ser)
ser.flushInput()  # 清空缓冲区
current_path = os.path.dirname(__file__)
os.chdir(current_path)


def main():
    log_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    log_name = 'Serial-%s-%s.log' % (serial_com, log_time)
    file_path = f'D:\\CRTlog\\{log_name}'
    # 特征码
    characteristic_codes = {'IMP_Encoder_PollingStream': '检测到无流打印',
                                }
    file = open(file_path, "w")

    ser.write('root\r\n'.encode())
    time.sleep(0.5)
    ser.write('aiqj@Y53L2303\r\n'.encode())
    time.sleep(1)
    ser.write('telnetd\r\n'.encode())

    while True:
        try:
            count = ser.inWaiting()  # 获取串口缓冲区数据

            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            local_date = time.strftime("%Y-%m-%d", time.localtime())
            if local_date not in log_time:
                # mylog.close()
                file.close()
                log_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                log_name = 'Serial-%s-%s.log' % (serial_com, log_time)
                # mylog = open(f'D:\\CRTlog\\{log_name}', mode='a', encoding='utf-8')
                file_path = f'D:\\CRTlog\\{log_name}'
                file = open(file_path, "w")

            elif count != 0:
                # serial_data = ser.read(ser.in_waiting).decode('utf-8')
                serial_data = ser.readline().decode('utf-8')
                serial_data = serial_data.strip()  # 取消换行
                print(f'[{localtime}] {serial_data}')  # 打印信息

                file.write(f'[{localtime}] {serial_data}\n')  # 写入文件
                file.flush()  # 刷新文件缓冲

                for code, news in characteristic_codes.items():
                    if code in serial_data:
                        url = countersign(ding_talk_robots['运营商测试组'])
                        send_dd_news(1, url, news)
                        time.sleep(1)


        except Exception as e:
            print(e)

        # time.sleep(0.1)


if __name__ == '__main__':
    main()
