# coding=utf-8
import locale
import os
import re
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

import xrs_serial
from by import AppiumBy as By
import image_properties
import ntp_util
import xrs_adb
import yaml_util
from adjacency_list import LinkedGraph
from data_store import toDictV5
from environment_variable import ruiboshi_excel, data_path
from image_properties import recognize_text
from my_decorator import retry, timer, printer, screenshot
from xrs_log import print
from automation_utils import bounds_to_coordinates, checkServerStatus, wakeUpPhone, boundsToCoordinates
from xrs_cgi import system_factoryDefault

locale.setlocale(locale.LC_CTYPE, 'chinese')

# 初始化参数，数据存放在data文件夹下，yaml文件类型
print(data_path + 'desired_caps.yaml')
desired_caps = yaml_util.YamlUtil(file_name=data_path + 'desired_caps.yaml').read_yaml()
app_info = yaml_util.YamlUtil(file_name=data_path + 'app_info.yaml').read_yaml()

# 显性等待时间，必须要等待2秒
WAITTIME = 2

'''
1、减少方法复杂度，过于负责则拿出来另写一个方法
2、
'''


class MobieProject:

    def __init__(self, app_name):
        """
        初始化方法，启动和家亲app，进入设备列表页面
        """
        checkServerStatus()  # 检查appuim服务器端口和手机连接状态
        wakeUpPhone()  # 唤醒解锁手机
        self.app_info = app_info[app_name]
        self.desired_caps = self.__returnAppPackName(desired_caps)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)  # 启动appuim客户端
        # 启动非本地服务端
        # self.driver = webdriver.Remote('http://192.168.123.147:4723/wd/hub', self.desired_caps)  # 启动appuim客户端
        time.sleep(10)  # 等待app启动
        self.mobile_phone = None
        self.LinkedGraph = LinkedGraph(sheetName=app_name)  # 创建邻接表
        self.allElemDict = toDictV5(ruiboshi_excel, sheetName=app_name)  # 缓存pwd的页面元素
        self.driver.implicitly_wait(20)  # 初始化隐形等待时间，最多等待20秒，超过20秒则报错

    def __returnAppPackName(self, desired_caps):
        # 为__init__方法提供self.desired_caps属性
        desired_caps['platformVersion'] = xrs_adb.popen('获取安卓版本')  # 更新手机安卓版本
        desired_caps.update(self.app_info)  # 加载手机app包名和active
        return desired_caps

    @retry(retries=2, delay=10)  # 当前执行返回未找到元素时，等待一段时间后再次执行
    @printer
    def clickControlV1(self, element: dict, content=None):
        """
        实现页面跳转，为goto方法提供基础方法
        :param element: 实现页面跳转的元素字典
        :param content: 输入框类型，输入的内容
        :return: 无
        """
        # 打印当前正在跳转的页面元素
        print(f"即将跳转至：\t{element}")

        # 等待wait时间，该时间由excel文件给出
        if element['wait']:
            print(f"等待{element['wait']}秒")
            time.sleep(element['wait'])

        # 判断控件类型是否为按钮,是则点击该元素
        if element['type'] in ['button', 'list_view']:
            self.onButtonClick(element, content)

        # 判断为输入框类型控件，是则在该元素输入content内容
        elif element['type'] == 'input_box':
            self.onInputChange(element, content)

        # 判断为持续检测时，则持续检测element的text属性，消失或超时时退出
        elif element['type'] == 'continuous_detection':
            self.continuous_detection(element['text'], duration=180)

        # 设备恢复出厂
        elif element['type'] == 'RTF':
            system_factoryDefault(mac=element['default_val'])

    def onButtonClick(self, element, content):
        # 遍历元素的属性值，判断是否为None，然后执行
        for attribute in ['text', 'resource_id', 'bounds']:

            # 如果元素的属性为空，则跳到下条属性
            if element[attribute] is None:
                continue

            elif attribute == 'resource_id':
                self.driver.find_element(By.ID, element[attribute]).click()

            elif attribute == 'text':
                # 从excel文件给出的text值，定位元素
                if not content:
                    self.driver.find_element(By.ANDROID_UIAUTOMATOR,
                                             F'new UiSelector().text("{element[attribute]}")').click()
                # 从程序中给出的text值，定位元素。此方法适用于设备列表中有多台设备的场景
                else:
                    self.driver.find_element(By.ANDROID_UIAUTOMATOR,
                                             F'new UiSelector().text("{content}")').click()
            # 通过坐标值点击元素，此方法被手机分辨率影响
            elif attribute == 'bounds':
                self.driver.tap(boundsToCoordinates(element[attribute]), 300)
            break

    def onInputChange(self, element, content):
        # 判断content是否为空，否则使用excel中默认值
        if content is None:
            content = element['default_val']

        for attribute in ['resource_id', 'text']:

            # 遍历元素的属性值，判断是否为None，然后执行
            if element[attribute] is None:
                continue

            elif attribute == 'resource_id':
                elem = self.driver.find_element(By.ID, element[attribute])
                elem.clear()
                elem.send_keys(content)

            elif attribute == 'text':
                elem = self.driver.find_element(By.ANDROID_UIAUTOMATOR,
                                                F'new UiSelector().text("{element[attribute]}")'
                                                )
                elem.clear()
                elem.send_keys(content)
            break

    @screenshot
    def continuous_detection(self, attribute: str, duration: int):
        # 持续检查元素的属性，直到属性不存在或者超时退出
        count = 0
        while self.is_element_exist(attribute):
            count += 1
            if count > duration: break

    def goto(self, *args) -> object:
        # 实现页面跳转，依赖于LinkedGraph类的寻路方法get_road_sign，依赖clickControlV1方法
        time.sleep(2)
        # 关闭弹窗，睿博士的弹窗
        if self.is_element_exist('提交'):
            self.clickControlV1({'resource_id': 'com.cmri.universalapp:id/iv_close'}, 'resource_id')

        # 执行goto前，先找到当前页面名称
        currentPageName = self.pwd()
        initial, destination = currentPageName, args[0]

        # 判断起始点与终点是否相同，相同则返回
        if initial == destination:
            return

        # 生成路径
        emel_list = self.LinkedGraph.get_road_sign(initial, destination)
        i = 1
        for emel in emel_list:
            # print(args)
            if emel['type'] in ['input_box', 'list_view'] and len(args) >= 2:  # 判断控件类型和形参个数
                content = args[i]
                i += 1
            else:
                content = None
            self.clickControlV1(emel, content)

    @retry(retries=2, delay=8)  # 当前执行返回未找到元素时，等待一段时间后再次执行
    def enterTo(self, control, content, mode):
        # 输入框控件
        if control is None:
            raise Exception("输入None")
        if mode == 'text':
            self.driver.find_element(By.ANDROID_UIAUTOMATOR,
                                     f'new UiSelector().text("{control}")'
                                     ).send_keys(content)
        elif mode == 'resource_id':
            self.driver.find_element(By.ID, control).send_keys(content)
        # elif mode == 'bounds':
        #     self.driver.tap(control, 300)

    def is_element_exist(self, element: str, times=3, wait=0, page_source=None) -> bool:
        """验证页面是否存在某个元素，用于判断页面是否跳转成功"""
        # 判断输入是否为int类型，是则转变为str类型
        if isinstance(element, int):
            element = str(element)
        count = 0
        while count < times:
            if page_source is None:
                souce = self.driver.page_source
            else:
                souce = page_source
            # print(element)
            if re.search(element, souce):  # 通过正则表示判断
                return True
            # if element in souce:
            #     return True
            else:
                count += 1
                time.sleep(wait)
        return False

    @timer
    def pwd(self):
        """找到当前所处页面"""
        page_source = self.driver.page_source  # 将is_element_exist方法需要用的页面元素提前缓存，优化运行效率
        if not xrs_adb.is_foreground(self.desired_caps['appPackage']):  # 判断app是否前台运行
            print('未检测到指定app')
        allElemDict = self.allElemDict  # 将pwd方法需要用的页面元素提前缓存，优化运行效率
        degreeOfRealism = dict()
        for pageName, elemList in allElemDict.items():
            degreeOfRealism[pageName] = 0
            for elem in elemList:
                # print(elem)   # 出现有的元素通过不了正则表达式
                for attribute in ['text', 'resource_id']:
                    if elem[attribute] is None:
                        continue
                    # 增加page_source形参是为了优化方法用时太长问题
                    elif self.is_element_exist(elem[attribute], times=1, page_source=page_source):
                        degreeOfRealism[pageName] += elem['weight']  # 加权
        for pageName, score in degreeOfRealism.items():  # 通过分数判断当前页面
            # 打印页面评分
            # print(pageName,':', score)
            if score == max(degreeOfRealism.values()):
                print(f'当前页面为<{pageName}>')
                return pageName

    def scroll_to_element(self, element, distance=0.2):
        """滑动屏幕找到元素element"""
        size = self.driver.get_window_size()
        # 当我第一次进入页面的时候：
        found = False
        count = 0
        old = None
        new = self.driver.page_source
        while not found and count != 1:
            if old == new:
                count += 1
            else:
                # 找元素
                if self.driver.page_source.find(element) != -1:
                    # print('找到了对应的内容')
                    found = True
                else:
                    # 找不到元素的时候，滑动，此时页面更新
                    self.driver.swipe(size['width'] * 0.5, size['height'] * 0.8, size['width'] * 0.5,
                                      size['height'] * (0.8 - distance), 200)
                    time.sleep(2)
                    # 更新old 的值。用new 的值更新old 的值
                    old = new
                    # 更新new 的值为滑动后的page_source
                    new = self.driver.page_source
        return found

    @timer
    def drag_until_element_disappears(self, attribute: dict, distance=0.2):
        """滑动屏幕，直到某个元素消失"""
        size = self.driver.get_window_size()
        count = 0
        if 'text' in attribute.keys():
            while self.driver.page_source.find(attribute['text']) != -1:
                self.driver.swipe(size['width'] * 0.5, size['height'] * 0.8, size['width'] * 0.5,
                                  size['height'] * (0.8 - distance),
                                  200)
                count += 1
                if count >= 10:
                    return False
        return True

    def long_press_element_by_uiautomator(self, selector, duration=2000):
        """
        在 Appium 中封装长按元素方法。

        Args:
            selector: 需要长按的 WebElement 对象的 UiSelector，可以是字符串或者 UiSelector 对象
            duration: 长按持续时间，默认为 2000 毫秒

        Returns:
            None
        """
        if isinstance(selector, str):
            selector = f'new UiSelector().text("{selector}")'
        element = self.driver.find_element(By.ANDROID_UIAUTOMATOR, selector)
        action = TouchAction(self.driver)
        action.long_press(element).wait(duration).release().perform()

    def find_nearest_element(self, attribute: dict, text_value):
        """通过resource_id定位多个元素，找到距离文本为text_value的元素最近的一个"""
        global elements
        if 'resource_id' in attribute.keys():
            # 找到所有具有给定 resource-id 的元素
            elements = self.driver.find_elements(By.ID, attribute['resource_id'])
        elif 'text' in attribute.keys():
            attribute_text = attribute['text']
            elements = self.driver.find_elements(By.ANDROID_UIAUTOMATOR,
                                                 f'new UiSelector().text("{attribute_text}")')

        # 获取参考元素的坐标
        if type(text_value) == type('string'):
            reference_element = self.driver.find_element(By.ANDROID_UIAUTOMATOR,
                                                         f'new UiSelector().text("{text_value}")')
        else:
            reference_element = text_value
        ref_location = reference_element.location

        # 计算其他元素的中心坐标并选择最接近参考元素的元素
        nearest_element, nearest_distance = None, float('inf')
        for element in elements:
            element_location = element.location
            element_size = element.size
            element_center = (element_location['x'] + element_size['width'] / 2,
                              element_location['y'] + element_size['height'] / 2)
            distance = ((element_center[0] - ref_location['x']) ** 2 +
                        (element_center[1] - ref_location['y']) ** 2) ** 0.5
            # print(element,element_center,distance,ref_location)
            if distance < nearest_distance:
                nearest_element, nearest_distance = element, distance

        return nearest_element

    def pinch_zoom(self, start, end, scale_factor=1.25, duration=500):
        action = TouchAction(self.driver)

        # 计算中心点
        start_x, start_y = start
        end_x, end_y = end
        mid_x = (start_x + end_x) // 2
        mid_y = (start_y + end_y) // 2

        # 第一根手指按下屏幕
        action.press(x=start_x, y=start_y)

        # 第二根手指按下屏幕并滑动到位置
        x1 = int(end_x + (end_x - mid_x) * (scale_factor - 1) / 2)
        y1 = int(end_y + (end_y - mid_y) * (scale_factor - 1) / 2)
        action.move_to(x=x1, y=y1).wait(duration)

        # 两根手指同时离开屏幕
        action.move_to(x=mid_x, y=mid_y).release()
        action.perform()

    def check_sdcard_recording_breakpoint(self, time_slot):
        """睿博士卡录像断点判断"""
        # 判断是否在回放页
        if self.pwd() != '回放页':
            raise Exception('当前页面不是回放页')
        os.system(xrs_adb.command_dict['手机截屏'])
        os.system(xrs_adb.command_dict['下载手机截屏'])

        # 截图，将回放进度条图片转变为时间字符串
        text_coords = recognize_text('C:\\Users\\Administrator\\Desktop\\video\\Screenshots\\screenshot.png',
                                     (0.44, 0.52, 0, 1))
        print(text_coords.keys())
        time_list = text_coords.keys()

        # 过滤非法时间，并返回时间区间
        time_list = [execution_time for execution_time in time_list if re.match(r'^([01][0-9]|2[0-3]):[0-5][0-9]$',
                                                                                execution_time)]
        time_range = (time_list[0], time_list[-1])

        # 获取屏幕分辨率，找到进度条的Y轴值
        screen_resolution = xrs_adb.get_screen_resolution()
        ruleview_y = screen_resolution[1] * 0.48

        # 判断需要检查的时间区间是否在页面中，不在则对应左移或者右移
        if ntp_util.compare_time(time_slot[0], time_range[0]):
            touch = TouchAction(self.driver)
            touch.press(x=100, y=ruleview_y).wait(1000).move_to(x=540, y=ruleview_y).release().perform()
            return self.check_sdcard_recording_breakpoint(time_slot)
        elif not ntp_util.compare_time(time_slot[0], time_range[1]):
            touch = TouchAction(self.driver)
            touch.press(x=900, y=ruleview_y).move_to(x=540, y=ruleview_y).release().perform()
            return self.check_sdcard_recording_breakpoint(time_slot)

        # 将时间换算为坐标X值，然后获取该区间内的所有像素的RGB值
        print('找到对应的区间')
        first_coordinate = (text_coords[time_range[0]][0], text_coords[time_range[1]][0])
        print(time_range, time_slot, first_coordinate)
        second_coordinate = ntp_util.get_coordinates(time_range, time_slot, first_coordinate)
        pixel_info = dict()
        for x in range(second_coordinate[0], second_coordinate[1], 1):
            pixel_info[(x, 80)] = image_properties.get_pixel_color('cropped.jpg', (x, 80))
        # print(pixel_info)

        # 将区间拖到中心，播放该区间的卡录像
        touch = TouchAction(self.driver)
        touch.press(x=second_coordinate[0], y=ruleview_y).wait(1000).move_to(x=540, y=ruleview_y).release().perform()

        # 遍历该RGB值的字典，判断是否有断点
        result = []
        for pixel, rgb in pixel_info.items():
            if sum(rgb) < 10:
                result.append(pixel)
        if result:
            return False
        else:
            return True

    def getElementText(self, attribute: dict):
        if 'resource_id' in attribute.keys():
            # 找到所有具有给定 resource-id 的元素
            element = self.driver.find_element(By.ID, attribute['resource_id'])
            return element.text

    def slide_to(self, attribute: dict, mode='vertical'):
        """拖动进度条"""
        if 'resource_id' in attribute.keys():
            # 找到所有具有给定 resource-id 的元素
            element = self.driver.find_element(By.ID, attribute['resource_id'])
            bounds = element.rect

            # 获取边界的左上角坐标
            x = bounds["x"]
            y = bounds["y"]

            # 获取边界的宽度和高度
            width = bounds["width"]
            height = bounds["height"]

            # 打印边界信息
            print("Bounds: x={}, y={}, width={}, height={}".format(x, y, width, height))


'''
1、完善邻接表
2、获取当前位置的方法
'''
if __name__ == "__main__":
    # 启动睿博士app，初始化测试环境
    system_factoryDefault(mac='5A:5A:00:75:DA:E7')
    xrs_serial.serial_bitstream("COM38", '断电', 1)
    xrs_serial.serial_bitstream("COM38", '上电', 1)
    project = MobieProject('睿博士')
    if project.is_element_exist('test_dev'):
        project.goto('删除设备')
    project.goto('扫一扫页')
    project.goto('设备扫描二维码', 'TP-LINK_04BB', 'cx123456', 'test_dev')
