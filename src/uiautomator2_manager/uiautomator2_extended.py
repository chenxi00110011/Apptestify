# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
from uiautomator2_automation_module import UiAutomator2TestDriver
import xml.etree.ElementTree as ET
from excel_utils import filter_df_and_write_excel
from config_module import ConfigManagerTest as test
from config_module import ConfigManagerRUIBOSHI as rui
from my_decorator import debug, retry, exception_handler


class Uiautomator2SophisticatedExecutor(UiAutomator2TestDriver):
    @debug(head="当前页面为：", print_flag=True)
    def get_current_page(self):
        # 使用dump_hierarchy方法获取当前页面的内容，并将其存储在page_content变量中
        page_content = self.driver.dump_hierarchy()
        # 调用digraph对象的compute_page_trust_score方法，并传入page_content作为参数
        # compute_page_trust_score方法将计算并返回信任分数最高的页面名
        return self.digraph.compute_page_trust_score(page_content)

    # @retry(retries=2)
    # @exception_handler
    def go_to_page(self, *args):
        """
        跳转到指定页面，处理必要的交互。
        """
        # 关闭广告（如果有的话）
        # self.close_popup()

        # 获取当前页面名称
        current_page_name = self.get_current_page()

        # 检查起始页面与目标页面是否相同
        if current_page_name == args[0]:
            return
        # 运行过程中检测到主屏幕，返回错误
        elif current_page_name == '手机主屏幕':
            raise Exception('APP崩溃')

            # 生成跳转路径
        path = self.digraph.get_shortest_path_for_app_pages(start_node=current_page_name, end_node=args[0])
        # print(path)
        args = args[1:]  # 移除目的地址
        # 遍历路径，执行跳转操作
        for step in path:
            print(step)
            content = None
            # 根据控件类型处理输入内容
            if step['控件类型'] in rui.UI_ELEMENTS and len(args) >= 1:
                content = args[0]
                args = args[1:]  # 移除已使用的参数
            # 执行点击或输入操作
            print("*" * 20, args, content)
            self.click_or_input(step, content)

    def exists_element(self, selector="text", value=None):
        global ui_object
        if selector == "text":
            ui_object = self.driver(text=value)
        elif selector == "resourceId":
            ui_object = self.driver(text=value)
        return ui_object.exists(timeout=0.2)

    def getAllElement(self, pageName):
        # 初始化一个字典，其键是表头，值是空列表
        data_dict = {header: [] for header in test.TABLE_HEADERS}
        print(data_dict)

        # 获取UI层次结构
        xml_str = self.driver.dump_hierarchy()
        print(type(xml_str))
        # 解析XML
        root = ET.fromstring(xml_str)
        # 遍历所有元素并打印它们的id和文本
        for elem in root.iter():
            for tag in data_dict.keys():
                if tag in elem.attrib:
                    data_dict[tag].append(elem.attrib[tag])
                elif tag == '页面名称':
                    data_dict[tag].append(pageName)
                else:
                    data_dict[tag].append('')
        # for v in df.values():
        #     print(len(v))
        # 修改filter_column值，进行过滤
        filter_df_and_write_excel(data_dict, filter_column='resource-id', filter_value='',
                                  output_file=test.PAGE_ELEMENT_FILE_PATH, sheet_name=test.ADJACENCY_LIST)


if __name__ == '__main__':
    d = Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '好威智')
    while True:
        pageName = input('请手动跳转页面，并输出页面名称：')
        d.getAllElement(pageName)
        # d.get_current_page()
