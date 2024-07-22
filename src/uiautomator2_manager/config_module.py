# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
from ntp_util import timestamp_to_date


def get_config(app_name: str):
    if app_name == "睿博士":
        return ConfigManagerRUIBOSHI
    elif app_name == "好威智":
        return ConfigManagerHOLOZ
    else:
        raise Exception("请输入app名称")


class ConfigManagerRUIBOSHI:
    # PAGE_ELEMENT_FILE_PATH = r'C:\Users\Administrator\PycharmProjects\AutoDriver_UIA2\venv\data\页面组件列表.xlsx'
    # 邻接表存放路径
    PAGE_ELEMENT_FILE_PATH = r'C:\Users\Administrator\PycharmProjects\AutoDriver_UIA2\venv\data\睿博士.xlsx'
    ADJACENCY_LIST = '邻接表'
    TRUST_LEVEL_TABLE = '置信表'
    # app包名
    APP_PACKAGE_NAME = 'com.zwcode.p6slite'
    # app活动名
    APP_ACTIVITY_NAME = '.activity.SplashActivity'
    # 所有列名
    TABLE_HEADERS = ['页面名称', '相邻页面', 'resource-id', 'bounds', 'text', '控件类型', '默认值', '置信度', '等待时间']
    # 判断置信度的列名
    ATTRIBUTE_LIST = ['text', 'resource-id']
    # 所有元素类型
    UI_CONTROLS_TYPE = ['按钮', '文本框', '勾选框', '单选按钮', '空值', '持续到页面跳转', '截图']
    # 需要输入内容的元素
    UI_ELEMENTS = ['文本框', '单选按钮', '截图']
    # 截图保存路径
    SCREENSHOT_PATH = rf"C:\Users\Administrator\Desktop\video\截图"
    # 存储手机截屏路径
    MOBILE_SCREEN_CAPTUREA = '/sdcard/DCIM/Screenshots/'
    # 日志目录
    LOGS_DIR = "C:/Users/Administrator/Desktop/logs"


class ConfigManagerHOLOZ:
    # PAGE_ELEMENT_FILE_PATH = r'C:\Users\Administrator\PycharmProjects\AutoDriver_UIA2\venv\data\页面组件列表.xlsx'
    PAGE_ELEMENT_FILE_PATH = r'C:\Users\Administrator\PycharmProjects\Apptestify\data\好威智.xlsx'
    ADJACENCY_LIST = '邻接表'
    TRUST_LEVEL_TABLE = '置信表'
    # app包名
    APP_PACKAGE_NAME = 'com.zwcloud.ruision.holowits'
    # app活动名
    APP_ACTIVITY_NAME = '.ui.modules.home.MainActivity'
    # 所有列名
    TABLE_HEADERS = ['页面名称', '相邻页面', 'resource-id', 'bounds', 'text', '控件类型', '默认值', '置信度', '等待时间']
    # 判断置信度的列名
    ATTRIBUTE_LIST = ['text', 'resource-id']
    # 所有元素类型
    UI_CONTROLS_TYPE = ['按钮', '文本框', '勾选框', '单选按钮', '空值', '持续到页面跳转', '截图']
    # 需要输入内容的元素
    UI_ELEMENTS = ['文本框', '单选按钮', '截图']
    # 截图保存路径
    SCREENSHOT_PATH = rf"C:\Users\Administrator\Desktop\video\截图"
    # 存储手机截屏路径
    MOBILE_SCREEN_CAPTUREA = '/sdcard/DCIM/Screenshots/'
    # 日志目录
    LOGS_DIR = "C:/Users/Administrator/Desktop/logs"


class ConfigManagerTest:
    # PAGE_ELEMENT_FILE_PATH = r'C:\Users\Administrator\PycharmProjects\AutoDriver_UIA2\venv\data\页面组件列表.xlsx'
    PAGE_ELEMENT_FILE_PATH = r'C:\Users\Administrator\PycharmProjects\Apptestify\data\test.xlsx'
    ADJACENCY_LIST = '邻接表'
    TRUST_LEVEL_TABLE = '置信表'
    APP_PACKAGE_NAME = 'com.zwcode.p6slite'
    APP_ACTIVITY_NAME = '.activity.SplashActivity'
    TABLE_HEADERS = ['页面名称', '相邻页面', 'resource-id', 'bounds', 'text', '控件类型', '默认值', '置信度', '等待时间']
    ATTRIBUTE_LIST = ['text', 'resource-id']
