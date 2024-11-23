# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""


"""
1. 把等待时间放在放在find_element 方法中实现，且分为两块
 一块是动态等待时间，在这段时间内，循环判断元素是否出现，出现就返回结果
 一块是固定等待时间，这个在click_or_input方法中实现，默认是等待1秒，还会从excel中读取
2. 把save_screenshot从新实现，用另一个方法替代
3. select_button方法从新实现，通过文本定位到附近的另一个元素，目前是通过坐标距离实现的
应该可以通过节点关系实现
"""

# uiautomator2_automation_module.py
from datetime import datetime
from ocr_extractor import extract_text_from_image, crop_image
import time
from uiautomator2 import connect, Device, _selector
from my_decorator import timer, forbidden_method, print_current_time, create_folder_if_not_exists
from adjacency_list_module import AppFlowGraph
from adb_commands import AdbManager as adb, AdbManager
from config_module import get_config
from my_decorator import screenshot, retry, printer, debug
from ui_hierarchy_utils import get_level_differences
import configparser
import os.path
import ntp_util
import re


class UiAutomator2TestDriver:

    @timer
    def __init__(self, androidDeviceID, app_name):
        # 从excel读取页面元素，并缓存
        self.allElemDict = None

        # 手机序列号
        self.androidDeviceID = androidDeviceID

        # 获取app相关配置参数
        self.config = get_config(app_name)

        # 获取包名
        self.appPackage = self.config.APP_PACKAGE_NAME

        # 手机连接
        self.driver = self.connect()  # 连接手机并启动app

        # 监听弹窗
        self.start_watcher()

        # 等待特定的Activity出现
        self.driver.wait_activity(self.config.APP_ACTIVITY_NAME, timeout=10)  # 等待10秒

        # 设置默认元素等待超时时间10秒
        self.driver.implicitly_wait(10)

        # 生成有向图
        self.digraph = AppFlowGraph(self.config)

        # 目录名称和文件名，用于截图
        self.did = 'XXX'
        self.title = {'wakeup_time': '', 'shootName': 'test.jpg'}
        self.run_parameters = {'rectangle': 0.5}

        # 显示等待时间，默认1秒
        self.WAIT_TIME = 1.0

        # 设置每次点击UI后再次点击之间延时1.5秒
        # self.driver.click_post_delay = 1.5

        # 停止监听弹窗
        self.driver.watcher.stop()

        # 定义弹窗处理字典
        self.popup_handlers = {
            "com.zwcode.p6slite:id/bg_dialog_obs_acti_iv": {
                "ok_button": "com.example.app:id/ok_button",
                "cancel_button": "com.example.app:id/cancel_button",
                "action": lambda: self.driver(resourceId="com.zwcode.p6slite:id/ic_close_cloud_free_dialog").click()
            },
            "com.example.app:id/another_popup_dialog": {
                "ok_button": "com.example.app:id/another_ok_button",
                "cancel_button": "com.example.app:id/another_cancel_button",
                "action": lambda: self.driver(resourceId="com.example.app:id/ok_button").click()
            },
            # 可以添加更多弹窗
        }

        # 读取配置文件
        self._config = self.read_config(r"C:\Users\Administrator\P2pServerTest\Apptestify\config\base.ini")

    def connect(self):
        # 点亮屏幕和解锁
        adb.execute_command(self.androidDeviceID, adb.LIGHT_UP_SCREEN)
        adb.execute_command(self.androidDeviceID, adb.UNLOCK_SCREEN)

        # 连接设备，这里使用设备的序列号，如果你没有提供序列号，将连接第一台可用的设备
        device = connect(self.androidDeviceID)

        # 关闭应用
        device.app_stop(self.appPackage)

        # 启动应用
        device.app_start(self.appPackage, wait=True)
        adb.set_default_input_method(self.androidDeviceID, 'io.appium.settings/.UnicodeIME')
        AdbManager.execute_command(self.androidDeviceID, command=AdbManager.TAP)

        return device

    def app_stop_(self):
        self.driver.app_stop(self.appPackage)

    def start_watcher(self):
        # 启用监听器
        # 监听手机重启后，弹出的USB传输选项
        self.driver.watcher("usb启动").when("传输文件 / Android Auto").click()
        self.driver.watcher("Wi-Fi网络信号差").when("不允许").click()
        self.driver.watcher.start()

    # @printer
    def localize_element(self, localization_method, edges, swap=False) -> _selector.UiObject:

        localization_dict = {
            'text': lambda: self.driver(text=edges['text']),
            'resource-id': lambda: self.driver(resourceId=edges['resource-id']),
            'className': lambda: self.driver(className=edges['className'])
            # 对于'bounds'，你需要定义相应的函数或逻辑
            # 'bounds': lambda: self.driver(...),  # 这里需要补全具体的逻辑
        }
        # 检查localization_method是否在字典的键中
        if localization_method in localization_dict.keys():
            if swap:
                # 拖动屏幕，找到对应的元素
                self.swipe_until_element_visible(edges[localization_method],
                                                 rectangle=self.run_parameters.get('rectangle'))
            # 隐式等待,默认10秒
            self.global_wait(localization_method, edges)
            # 调用字典中对应的函数
            return localization_dict[localization_method]()
        else:
            # 如果localization_method不在字典中，可以抛出一个异常或返回None
            raise ValueError(f"Invalid localization method: {localization_method}")

    @printer
    def find_element(self, edges: dict, swap=False) -> _selector.UiObject:
        """
        根据提供的边缘信息字典定位元素。
        参数:
        edges (dict): 包含定位信息的字典，键为定位方法（如'text', 'id', 'bounds'），值为对应的定位值。
        返回:
        None: 该方法不返回任何值，而是直接通过 self.localize_element 方法定位元素。
        注意：该方法会遍历预定义的定位方法列表，找到第一个在 edges 字典中不为 None 的定位方法，并使用它定位元素。
        """
        localization_method_list = self.config.ATTRIBUTE_LIST
        localization_method = None

        # 遍历预定义的定位方法列表
        for method in localization_method_list:
            # print(method)

            # 检查 edges 字典中是否含有method
            if method not in edges.keys():
                continue

            # 检查 edges 字典中当前定位方法对应的值是否为 None 和 nan
            if edges[method] is not None and edges[method] == edges[method]:
                # 如果不为 None，则设置 localization_method 为当前定位方法
                localization_method = method
                # 跳出循环，不再继续检查其他定位方法
                break

                # 调用 localize_element 方法进行元素定位
        # print(localization_method)
        if localization_method is not None:
            # 当前页面跳转到下一跳页面，无需定位元素时，直接返回
            return self.localize_element(localization_method, edges, swap)

    # 定义处理弹窗的函数
    def handle_popup(self):
        for popup_id, handler in self.popup_handlers.items():
            if self.driver(resourceId=popup_id).exists:
                # 执行相应的处理逻辑
                handler["action"]()
                print(f"弹窗 {popup_id} 已处理")
                return True
        return False

    def global_wait(self, localization_method, edges, times=10):
        """
        隐式等待

        :param self: 当前类实例的引用。
        :param localization_method: 在屏幕上定位元素所使用的方法。
                                     这可能是指通过ID、类名、文本或其他属性来定位元素的方法。
        :param edges: 定义等待区域的边界，这可能是一个包含屏幕坐标的元组或列表，
                      用于限定等待元素出现的屏幕区域。
        """
        while not self.exists_element(selector=localization_method,
                                      value=edges.get(localization_method), timeout=1.0) and times >= 0:
            times -= 1

    # @printer
    def swipe_until_element_visible(self, attr, rectangle=1.0):
        """滑动屏幕找到元素element"""
        size = self.driver.window_size()
        # 当我第一次进入页面的时候：
        found = False
        count = 0
        old_page = None
        new_page = self.driver.dump_hierarchy()
        new_page = new_page[:int(len(new_page) * rectangle)]
        while not found and count < 3:
            if old_page == new_page:
                count += 1
            else:
                # 找元素
                if attr in new_page:
                    # print('找到了对应的内容')
                    found = True
                else:
                    # 找不到元素的时候，滑动，此时页面更新
                    self.driver.swipe_ext('up', scale=0.25, duration=0.1)
                    # 更新old 的值。用new 的值更新old 的值
                    old_page = new_page
                    # 更新new 的值为滑动后的page_source
                    time.sleep(0.1)
                    new_page = self.driver.dump_hierarchy()
                    new_page = new_page[:int(len(new_page) * rectangle)]
        return found

    def input_text_to_element(self, element, content, step=None):
        """
        向指定的输入框元素发送内容。

        :param element: 输入框元素
        :param content: 要输入的内容
        :param step: 包含默认值等信息的字典（可选）
        """
        # 清空输入框的当前内容
        element.set_text('')

        # 如果提供了内容，则发送内容到输入框
        if content:
            element.send_keys(content)
            # 如果没有提供内容但提供了step字典，并且step字典中包含默认值，则发送默认值到输入框
        elif step and '默认值' in step:
            element.send_keys(step['默认值'])
        # 如果需要，你可以发送一个回车键事件来结束输入
        self.driver.press("enter")

    def check_and_click_checkbox(self, element):
        # 假设element.info['checked']可以正确获取checked属性的值
        is_checked = element.info['checked']
        # 预设值的目标
        target = self.title.get("checked")
        # 如果CheckBox与目标不一致，则点击它
        if is_checked != target:
            element.click()

    def handleRadioGroupSelection(self, content):
        # 如果提供了内容，则点击该内容的元素
        if content:
            element = self.localize_element(localization_method='text', edges={'text': content})
            element.click()
        else:
            raise Exception("单选按钮未提供content")

    @timer
    def stayUntilJumpToNewPage(self, step):
        if step.get('默认值') == step.get('默认值') and step.get('默认值'):
            timeout = step['默认值']
        else:
            timeout = 10
        timeout = int(timeout)
        start_time = time.time()
        # 检查页面是否存在文本
        while self.exists_element(selector='text', value=step.get('text')) or timeout >= 0:
            timeout -= 1
        end_time = time.time()
        self.title['wakeup_time'] = "{:.1f}秒".format(end_time - start_time)

    @print_current_time
    @screenshot(shot_path=rf"C:\Users\Administrator\Desktop\video\截图")
    def save_screenshot(self):
        """
        截取设备屏幕并保存到指定路径。
        参数:
        device (uiautomator2.Device): 已连接的 uiautomator2 设备对象。
        save_path (str): 截图保存的路径和文件名。
        返回:
        None
        """
        print("手机截图")
        return self

    def save_screenshotV1(self, bounds=None):
        """
        保存截图到指定路径。

        1. 从配置文件中获取基础路径。
        2. 获取当前日期。
        3. 拼接完整的路径。
        4. 确保目录存在。
        5. 保存截图到指定路径。
        """
        # 从配置文件中获取基础路径
        base_path = self._config.get("睿博士APP", "shot_path")

        # 获取当前日期，格式为 YYYY-MM-DD
        date = ntp_util.timestamp_to_date()

        # 拼接完整的路径
        full_path = os.path.join(base_path, self.androidDeviceID, self.did, date)

        # 确保目录存在
        create_folder_if_not_exists(full_path)

        # 生成截图文件名
        screenshot_filename = self.title.get('shootName')

        # 拼接完整的文件路径
        screenshot_path = os.path.join(full_path, screenshot_filename)

        # 保存截图
        self.driver.screenshot(screenshot_path)

        # 判断是否需要对图片进行处理
        if bounds is None:
            print(">>>here----")
            return screenshot_path

        # 对图片进行裁剪
        crop_image(screenshot_path, bounds['left'], bounds['top'], bounds['right'], bounds['bottom'], output=True,
                   target_width=300, target_height=300)
        print(">>>here")
        return screenshot_path

    def exists_element(self, selector="text", value=None, timeout=0.2):
        global ui_object
        if selector == "text":
            ui_object = self.driver(text=value)
        elif selector == "resource-id":
            ui_object = self.driver(resourceId=value)
        elif selector == "className":
            ui_object = self.driver(className=value)
        return ui_object.exists(timeout=timeout)

    @staticmethod
    def read_config(file_path):
        """
        读取 INI 配置文件。

        :param file_path: INI 文件的路径
        :return: 配置对象
        """
        config = configparser.ConfigParser()
        with open(file_path, 'r', encoding='utf-8') as file:
            config.read_file(file)
        return config

    def get_closest_element(self, text: str, elements, mode=None) -> _selector.UiObject:
        """
        获取距离给定点最近的元素。
        """

        def get_element_center_coordinates(element):
            # 获取元素的坐标中心
            bounds = element.info['bounds']
            # print(bounds)
            # 计算中心坐标
            center_x = (bounds['left'] + bounds['right']) // 2
            center_y = (bounds['top'] + bounds['bottom']) // 2
            # 将中心坐标存储在变量中
            center_coordinates = (center_x, center_y)
            # print(center_coordinates)
            return center_coordinates

        def calculate_distance_between_coordinates(coord1, coord2):
            """
            计算两个坐标之间的距离（使用欧几里得距离）。
            参数:
            coord1 (tuple): 包含两个数值的元组，表示第一个坐标 (x1, y1)。
            coord2 (tuple): 包含两个数值的元组，表示第二个坐标 (x2, y2)。
            返回:
            float: 两个坐标之间的欧几里得距离。
            """
            x1, y1 = coord1
            x2, y2 = coord2
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            return distance

        elem1 = self.localize_element(localization_method='text', edges={'text': text})
        coord1 = get_element_center_coordinates(elem1)
        coord2 = None
        elem_coordinate = {}

        # 检查 elements是否是列表，不是就改为列表类型
        if not isinstance(elements, list):
            elements = [elements]

        for elem2 in elements:
            # 获取元素的坐标
            # print("-" * 10, ">走这")
            coord2 = get_element_center_coordinates(elem2)
            # 模式是向下查找，并且元素的Y轴坐标小于锚点
            if mode == 'DOWN' and coord2[1] - coord1[1] < -50:
                continue
            # 模式是向上查找，并且元素的Y轴坐标大于锚点
            elif mode == 'UP' and coord2[1] - coord1[1] > 50:
                continue
            elem_coordinate[elem2] = calculate_distance_between_coordinates(coord1, coord2)

        # print("coord1, coord2: ", coord1, coord2)
        # print(isinstance(elements, list))
        # print("elements: ", elements)
        # print("elem_coordinate: ", elem_coordinate)
        min_key = min(elem_coordinate, key=lambda k: elem_coordinate[k])
        return min_key

    def select_button(self, selection_criteria: dict, content=None) -> None:
        if content is not None:
            # 拖到屏幕找到对应元素
            self.localize_element(localization_method='text', edges={'text': content}, swap=True)
            # 收集所有符合条件的控件
            by = ""
            if selection_criteria.get("resource-id") == selection_criteria.get("resource-id"):
                # print('selection_criteria.get("resource-id"):', selection_criteria.get("resource-id"))
                by = "resource-id"
                localized_elements = self.localize_element(localization_method=by, edges=selection_criteria)
            else:
                by = "text"
                localized_elements = self.localize_element(localization_method=by, edges=selection_criteria)

            # # 定位离content文字最近的控件
            # closest_element = self.get_closest_element(text=content, elements=localized_elements, mode='DOWN')
            # print(closest_element)
            # closest_element.click()

            # 判断类型是否为列表，不是则直接点击
            # print(type(localized_elements), len(localized_elements))
            if len(localized_elements) > 1:
                # 找到层级最近元素的下标
                index = get_level_differences(self.driver, content, selection_criteria[by], by)
                localized_elements[index].click()
            elif len(localized_elements) == 1:
                localized_elements.click()
            else:
                raise Exception("未找到对应的元素")

        else:
            # 未提供定位元素的锚点，则点击第一个元素
            localized_elements = self.localize_element(localization_method="resource-id", edges=selection_criteria)
            localized_elements.click()

    def click_variable_text(self, pattern: str):
        # 用于定位文本内容可变的元素，例如蓝牙配网里的DID等
        self.localize_element(localization_method='text', edges={'text': pattern}, swap=True).click()

    def get_element_text(self, element: _selector.UiObject):
        val = element.get_text()
        self.title['text'] = val

    def click_element_by_content_desc(self, content=None) -> None:
        print('#' * 100, content)
        if content is not None:
            # 找到带content文字的元素
            element = self.localize_element(localization_method='contentDesc',
                                            edges={'contentDesc': content})
            element.click()
        else:
            raise Exception("未提供定位信息，请填写默认值")

    def drag_timeline(self, timeLineId: str, tvTimeId: str, target_time: str, offset=10, duration=0.2):
        """
        拖动时间轴到目标时间。

        :param timeLineId: 时间轴元素的资源ID
        :param tvTimeId: 当前时间显示元素的资源ID
        :param target_time: 目标时间（格式为 "HH:MM:SS"）
        :param offset: 每次拖动的偏移量
        :param duration: 拖动持续时间（秒）
        """
        # 查找时间轴元素
        timeline = self.driver(resourceId=timeLineId)
        tvtime = self.driver(resourceId=tvTimeId)

        # 确保时间轴元素和当前时间元素存在
        if not (timeline.exists and tvtime.exists):
            print("时间轴元素或当前时间元素未找到，请检查资源ID或UI层次结构。")
            return

        # 获取当前时间和目标时间的时间戳
        def parse_time(time_str):
            h, m, s = map(int, time_str.split(':'))
            return h * 3600 + m * 60 + s

        current_timestamp = parse_time(tvtime.get_text())
        target_timestamp = parse_time(target_time)

        # 获取时间轴的边界信息
        timeline_bounds = timeline.info['bounds']
        x_center = (timeline_bounds['left'] + timeline_bounds['right']) // 2
        y_center = (timeline_bounds['top'] + timeline_bounds['bottom']) // 2  # 时间轴的中心

        # 初始化拖动次数和拖动系数
        drag_left = 0
        drag_right = 0
        drag_coefficient = 1

        # 拖动时间轴直到达到目标时间
        while abs(current_timestamp - target_timestamp) > 10:  # 允许10秒的误差
            # 计算拖动系数
            if drag_left == 0 or drag_right == 0:
                drag_coefficient = drag_coefficient * 2
            else:
                # 反向时初始化拖动次数和拖动系数
                drag_left = 0
                drag_right = 0
                drag_coefficient = 1

            # 控制拖动距离在范围内
            if x_center - drag_coefficient * offset <= 0:
                drag_coefficient //= 2
            elif drag_coefficient < 1:
                drag_coefficient = 1

            # 判断目标距离是否小于60秒
            if abs(current_timestamp - target_timestamp) <= 60:
                offset = 2
                drag_coefficient = 1
            elif abs(current_timestamp - target_timestamp) <= 600:
                offset = 10
                drag_coefficient = 1

            if current_timestamp > target_timestamp:
                # 向左拖动
                self.driver.swipe(x_center, y_center, x_center + drag_coefficient * offset, y_center, duration=duration)
                drag_left += 1
            else:
                # 向右拖动
                self.driver.swipe(x_center, y_center, x_center - drag_coefficient * offset, y_center, duration=duration)
                drag_right += 1

            # 更新当前时间
            current_timestamp = parse_time(tvtime.get_text())

        print(f"时间轴已拖动到目标时间: {target_time}")

    def switch_to_date(self, date_str: str):
        """
        后续需要优化，使用元素定位区域，然后再裁剪图片和滑动元素
        """
        # 获取手机显示的月份
        date1_str = self.driver(resourceId="com.zwcode.p6slite:id/tv_current_time").get_text()

        # 将字符串解析为 datetime 对象
        date_time_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        # 将 datetime 对象转换为时间元组
        time_tuple = date_time_obj.timetuple()

        # 提取年月
        year_mount = f"{time_tuple[0]}-{time_tuple[1]:02d}"

        while year_mount != date1_str:
            print(year_mount, date1_str)
            if not year_mount:
                return
            if year_mount > date1_str:
                self.driver(resourceId="com.zwcode.p6slite:id/iv_next_month").click()
            if year_mount < date1_str:
                self.driver(resourceId="com.zwcode.p6slite:id/iv_previous_month").click()
            # 获取手机显示的月份
            date1_str = self.driver(resourceId="com.zwcode.p6slite:id/tv_current_time").get_text()

        # 日期所处获取日历的坐标
        week_of_month, weekday = ntp_util.get_calendar_position(date_str)
        print("week_of_month, weekday", week_of_month, weekday)

        # 通过父元素，className，index来定位日历元素
        # 定位日历元素
        calendar_element = (self.driver(resourceId="com.zwcode.p6slite:id/calendarview").
                            child(className="android.widget.LinearLayout", index=0))[0]

        # 定位周元素
        week_element = calendar_element.child(className="android.widget.LinearLayout", index=week_of_month + 1)

        # 定位day元素，并点击
        week_element.child(className="android.view.View", index=weekday + 1).click()

    def switch_to_time(self, date_str: str):
        # 将字符串解析为 datetime 对象
        date_time_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        # 将 datetime 对象转换为时间元组
        time_tuple = date_time_obj.timetuple()
        # 定位时间元素，滑动
        while True:
            # 先截图，然后通过OCR识别图片中的文字
            time.sleep(1)
            screenshot_path = self.save_screenshotV1()

            # 裁剪区域的坐标 (左, 上, 右, 下)
            crop_area = (0, 2010, 1080, 2080)

            # 进行 OCR
            text = extract_text_from_image(screenshot_path, lang='chi_sim', crop_area=crop_area)
            words = text.split()  # 默认以空格为分隔符

            # 使用列表推导式去掉“时”、“分”、“秒”
            cleaned_time_parts = [part.replace('时', '').replace('分', '').replace('秒', '') for part in words]

            # 计算当前时分秒与目标的差值
            hour_difference = int(cleaned_time_parts[0]) - time_tuple[3]
            minute_difference = int(cleaned_time_parts[1]) - time_tuple[4]
            second_difference = int(cleaned_time_parts[2]) - time_tuple[5]

            if hour_difference == 0 and minute_difference == 0 and second_difference == 0:
                break

            # 滑动定位到时间
            if hour_difference:
                for i in range((24 - hour_difference) % 24):
                    self.driver.swipe(180, 2043, 180, 2043 - 70, duration=0.1)
            if minute_difference:
                for i in range((60 - minute_difference) % 60):
                    self.driver.swipe(540, 2043, 540, 2043 - 70, duration=0.1)
            if second_difference:
                for i in range((60 - second_difference) % 60):
                    self.driver.swipe(900, 2043, 900, 2043 - 70, duration=0.1)

    def open_notifications(self):
        # 打开通知栏
        screen_height = self.driver.info['displayHeight']
        screen_width = self.driver.info['displayWidth']
        self.driver.swipe(screen_width // 2, 0, screen_width // 2, screen_height * 0.75)

    def close_notifications(self):
        # 关闭通知栏
        screen_height = self.driver.info['displayHeight']
        screen_width = self.driver.info['displayWidth']
        self.driver.swipe(screen_width // 2, screen_height, screen_width // 2, screen_height * 0.25)

    @staticmethod
    @printer
    def optional_button(element):
        # 如果元素存在，则点击，否则直接返回
        if element.exists():
            element.click()

    def click_or_input(self, step, content=None):
        """
            根据步骤信息执行点击或输入操作。

            Args:
                step (dict): 包含控件信息的字典，如控件类型、定位方式等。
                content (str, optional): 如果需要输入内容，则为输入内容。默认为None。

            Returns:
                None
            """
        # 检查弹窗
        self.handle_popup()

        # 根据步骤信息查找页面元素
        element = self.find_element(step)
        # 检查控件类型并执行相应操作
        if step['控件类型'] == '空值':
            # 如果控件类型是为空值，则直接返回
            return
        elif step['控件类型'] == '文本框':
            # 如果控件类型是文本框，则向该元素发送内容（输入文本）
            self.input_text_to_element(element, content, step)
        elif step['控件类型'] == '按钮':
            # 如果控件类型是按钮，则点击该元素
            element.click()
        elif step['控件类型'] == '非必选按钮':
            # 如果控件类型是可选按钮，则先判断控件是否存在
            self.optional_button(element)
        elif step['控件类型'] == '勾选框':
            # 如果控件类型是勾选框，判断状态后再勾选该元素
            self.check_and_click_checkbox(element)
        elif step['控件类型'] == '单选按钮':
            # 如果控件类型是单选按钮,判断是否有值，有则点击该值对应的按钮，无则点击第一个按钮
            self.select_button(step, content=content)
        elif step['控件类型'] == '持续到页面跳转':
            self.stayUntilJumpToNewPage(step)
        elif step['控件类型'] == '截图':
            # 截取屏幕截图
            self.save_screenshot()  # 使用截图方法
        elif step['控件类型'] == '获取文本':
            # 获取属性值
            self.get_element_text(element)
        elif step['控件类型'] == 'contentDesc':
            # 基于元素的“可访问性描述”（Accessibility Description）来识别界面组件
            self.click_element_by_content_desc(content=content)
        elif step['控件类型'] == '可变文本':
            self.click_variable_text(content)
        elif step['控件类型'] == '打开通知栏':
            self.open_notifications()
        elif step['控件类型'] == '关闭通知栏':
            self.close_notifications()
        elif step['控件类型'] == '选择日期':
            self.switch_to_date(content)
        elif step['控件类型'] == '选择时间':
            self.switch_to_time(content)
        elif step['控件类型'] == '拖动时间轴':
            if content:
                self.drag_timeline("com.zwcode.p6slite:id/time_line_view",
                                   "com.zwcode.p6slite:id/tv_time", target_time=content, duration=0.1)
        elif step['控件类型'] == '切换网络':
            if content:
                _ssid = content[0]
                _pwd = content[1]
                AdbManager.connect_network(self.androidDeviceID, _ssid, _pwd)
            else:
                raise Exception("未检测到参数：Wi-Fi名称和密码")
        # 判断等待时间不为nan
        if step['等待时间'] == step['等待时间']:
            time.sleep(step['等待时间'])
        else:
            time.sleep(self.WAIT_TIME)

            # 注释说明：
        # 1. `self.find_element(step)` 应该是一个根据步骤信息定位页面元素的方法，
        # 2. `step['控件类型']` 假设步骤字典中包含一个键为 '控件类型' 的项，
        #    其值指示了元素的类型（如 'input_box' 或 'button'）。
        # 3. `element.send_keys(content)` 用于向输入框发送文本的方法。
        # 4. `element.click()` 用于点击按钮的方法。

    @printer
    @retry(retries=3, delay=2)
    def get_current_page(self):

        # 使用dump_hierarchy方法获取当前页面的内容，并将其存储在page_content变量中
        page_content = self.driver.dump_hierarchy()
        # 调用digraph对象的compute_page_trust_score方法，并传入page_content作为参数
        # compute_page_trust_score方法将计算并返回信任分数最高的页面名
        return self.digraph.compute_page_trust_score(page_content)

    @staticmethod
    def demo_01():
        from uiautomator2_manager import uiautomator2_extended
        d = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', 'com.zwcode.p6slite')
        d.go_to_page("直播")

    @staticmethod
    def demo_02():
        # 根据DID来进入直播
        from uiautomator2_manager import uiautomator2_extended
        d = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', 'com.zwcode.p6slite')
        # elems = d.driver(resourceId="com.zwcode.p6slite:id/item_device_play")
        arrt = {"resource-id": "com.zwcode.p6slite:id/item_device_snapshot"}
        elems = d.localize_element(localization_method="resource-id", edges=arrt)
        time.sleep(5)
        elem = d.get_closest_element(text="000602", elements=elems)
        print(elem)
        elem.click()


if __name__ == '__main__':
    from uiautomator2_manager import uiautomator2_extended
    import re

    d = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(5)
    d.go_to_page('设备设置', '000244')
    d.go_to_page('获取电量')
    print(d.title)
    match = re.search(r'\d+', d.title['text'])
    if match:
        battery_percentage = int(match.group())
        print("电池电量:", battery_percentage, "%")
