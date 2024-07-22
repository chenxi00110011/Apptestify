# -*- coding: utf-8 -*-
"""
-用于存放app自动化的静态方法
Author:陈熙
Date:2024年2月27日
"""
import os
import traceback

import openpyxl
from openpyxl.utils import get_column_letter

import xrs_adb
from my_decorator import printer


@printer
def bounds_to_coordinates(bounds_string, screen_resolution=(1080, 2340)):
    """
    将坐标字符串转换为坐标点。

    参数:
    bounds_string (str): 坐标字符串，例如 "[945,123][1035,213]"
    screen_resolution (tuple): 屏幕分辨率，例如 (1080, 2340)

    返回值:
    list: 坐标点列表，例如 [(x, y)]
    """

    # 根据屏幕分辨率定义偏差值
    deviation_values = {
        (1080, 2340): (1, 1),
        (720, 1600): (1.05, 0.938),
        # 在这里添加更多屏幕分辨率及其对应的偏差值
    }
    x_strings, y_strings = list(), list()
    # 获取给定屏幕分辨率的偏差值，如果没有匹配项，则使用默认值 (1, 1)
    scale_factor_x, scale_factor_y = deviation_values.get(screen_resolution, (1, 1))

    # 从坐标字符串中提取坐标
    coordinates_strings = bounds_string.strip('[]').split('][')
    x_strings.append(coordinates_strings[0].split(',')[0])
    x_strings.append(coordinates_strings[1].split(',')[0])
    y_strings.append(coordinates_strings[0].split(',')[1])
    y_strings.append(coordinates_strings[1].split(',')[1])

    # 将字符串转换为整数并计算平均值
    x_average = int((int(x_strings[0]) + int(x_strings[1])) / 2)
    y_average = int((int(y_strings[0]) + int(y_strings[1])) / 2)

    # 应用偏差值并根据物理屏幕尺寸进行缩放
    x_coordinate = int((x_average * screen_resolution[0] * scale_factor_x) / 1080)
    y_coordinate = int((y_average * screen_resolution[1] * scale_factor_y) / 2340)

    # 返回结果，坐标点列表
    return [(x_coordinate, y_coordinate)]


def boundsToCoordinates(bounds):
    # 将坐标字符串，转为坐标点。例如[945,123][1035,213]，变为[(x,y)]格式
    physical_size = xrs_adb.get_screen_resolution()
    if physical_size == (1080, 2340):
        deviation_value_x, deviation_value_y = 1, 1
    elif physical_size == (720, 1600):
        deviation_value_x, deviation_value_y = 1.05, 0.938
    result = bounds.split('[')
    result = ','.join(result)
    result = result.split(']')
    result = ''.join(result)
    result = result.split(',')
    x = int((int(result[1]) + int(result[3])) * (physical_size[0] * deviation_value_x / 1080) / 2)
    y = int((int(result[2]) + int(result[4])) * (physical_size[1] * deviation_value_y / 2340) / 2)
    return [(x, y)]


def wakeUpPhone():
    xrs_adb.wakeUpScreen()  # 点亮屏幕
    os.system(xrs_adb.command_dict['滑屏解锁'])  # 滑屏解锁


def checkServerStatus():
    # 判断手机是已连接本地电脑
    if xrs_adb.check_device_connection():  # 检查安卓手机是否已连接
        print('Android device is connected.')
    else:
        raise Exception('No Android device found, or the device is not properly connected.')
        # print("No Android device found, or the device is not properly connected.")

    if xrs_adb.check_appium_server(4723):  # 检查appuim服务器端口
        print('Appium server is running.')
    else:
        raise Exception('Appium server is not running.')


def is_element_checkable(element):
    """判断元素是否勾选，true表示已勾选"""
    checkable_attr = element.get_attribute('checked')
    return checkable_attr == 'true'


def get_element_data(element, excel_file_path, vertex_name, sheetName):
    """
       获取App页面元素数据，并将其存储在Excel文件中
       :param sheetName:
       :param vertex_name:
       :param element:
       :param excel_file_path: Excel文件路径
    """
    try:
        # 打开Excel工作簿
        workbook = openpyxl.load_workbook(excel_file_path)
        worksheet = workbook[sheetName]
        # 检索最小的空行号
        min_empty_row = 2
        while worksheet[f'A{min_empty_row}'].value:
            min_empty_row += 1
        element_dict = {
            '顶点': vertex_name,
            '邻近点': None,
            'resource_id': element.get_attribute('resource-id'),
            'bounds': element.get_attribute('bounds'),
            'text': element.text,
            'type': None,
            'default_val': None,
            'weight': 1,
            'wait': None
        }
        for idx, key in enumerate(element_dict, start=1):
            col_letter = get_column_letter(idx)
            # print(col_letter,min_empty_row)
            worksheet[f'{col_letter}{min_empty_row}'] = element_dict[key]
        # 保存工作簿
        workbook.save(excel_file_path)

    except Exception as e:
        traceback.print_exc()
    print(e)


if __name__ == '__main__':
    bounds_to_coordinates('[100,100][200,200]')
