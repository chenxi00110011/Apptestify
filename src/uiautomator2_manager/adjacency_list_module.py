# -*- coding: utf-8 -*-
"""
-
Author:chenxi
Date:2024年3月29日
"""
import time

import networkx as nx
from excel_utils import AdjacencyListHandler
import matplotlib.pyplot as plt
from my_decorator import timer, print_list_items


class AppFlowGraph:

    # 类的初始化方法，当创建这个类的实例时，会自动调用此方法
    # @timer
    def __init__(self, config):
        self.config = config
        # 初始化实例变量file_path，从ConfigManager类中的PAGE_ELEMENT_FILE_PATH常量获取值
        # 假设exc是ConfigManager类的实例或者该常量在全局作用域内定义
        self.file_path = self.config.PAGE_ELEMENT_FILE_PATH

        # 初始化实例变量adjacency_list_name，从ConfigManager类中的ADJACENCY_LIST常量获取值
        self.adjacency_list_name = self.config.ADJACENCY_LIST

        # 初始化实例变量trust_Level_table，从ConfigManager类中的TRUST_LEVEL_TABLE常量获取值
        self.trust_Level_table = self.config.TRUST_LEVEL_TABLE

        # 调用get_page_element方法，传入邻接表的sheet名，初始化实例变量page_element_adj
        # 假设get_page_element方法返回一个AdjacencyListHandler对象
        self.page_element_adj = self.get_page_element(sheetName=self.adjacency_list_name)

        # 调用get_page_element方法，传入信任级别表的sheet名，初始化实例变量data_frame_trust_Level_table
        self.data_frame_trust_Level_table = self.get_page_element(sheetName=self.trust_Level_table)

        # 初始化实例变量digraph，初始值为None，表示一个尚未创建的有向图
        self.digraph = None

        # 初始化实例变量allElemDict，初始值为None，可能用于存储从Excel中获取的所有元素的字典
        self.allElemDict = None

        # 调用create_digraph方法，使用已经初始化的page_element_adj来创建有向图
        # 假设create_digraph方法内部会修改self.digraph变量，使其成为有向图对象
        self.create_digraph()  # 创建有向图

        # 调用get_page_element_all_dict方法，获取Excel中的所有元素，并更新allElemDict实例变量
        # 假设get_page_element_all_dict方法会返回所有元素的字典，并赋值给self.allElemDict
        self.get_page_element_all_dict()  # 获取并存储Excel中的所有元素

    # 定义一个方法，用于从Excel文件中获取指定sheet页的内容
    def get_page_element(self, sheetName):
        # 创建一个AdjacencyListHandler对象，用于处理页面元素邻接表
        # 传入file_path（文件路径）和sheetName（工作表名）作为参数
        # 返回这个处理器对象，该对象可能包含了对Excel文件中指定sheet页内容的处理逻辑
        return AdjacencyListHandler(self.file_path, sheetName)

    def create_digraph(self):
        # 创建一个空的有向图对象
        directed_graph = nx.DiGraph()

        # 从page_element_adj对象中获取所有的页面节点名
        app_page_nodes = self.page_element_adj.getPageName()

        # 从page_element_adj对象中获取所有边的信息，这里假设getEdges().keys()返回的是一个边的列表
        app_page_transitions = self.page_element_adj.getEdges().keys()

        # 将页面节点名添加到有向图中
        directed_graph.add_nodes_from(app_page_nodes)  # 这里的add_nodes_from用于添加多个节点

        # 添加边到有向图中，注意有向图的边是带有方向的
        # 这里直接添加app_page_transitions作为边可能存在问题，因为add_edges_from期望的是边的元组列表
        # 如果app_page_transitions直接就是边的元组列表，那么这行代码是正确的
        # 如果不是，则需要从app_page_transitions中提取出正确的边信息（即源节点和目标节点的元组）
        directed_graph.add_edges_from(app_page_transitions)  # 添加多条有向边

        # 将创建好的有向图赋值给类的实例变量self.digraph，以便后续使用
        self.digraph = directed_graph

    def get_page_element_all_dict(self):
        # 从Excel文件中读取所有页面元素，并存储到self.allElemDict字典中
        self.allElemDict = self.data_frame_trust_Level_table.read_all_elements_from_excel()

    def show_directed_graph_visualization(self):
        # 设置matplotlib参数以支持中文显示
        # 修改matplotlib的默认字体设置，使用'SimHei'黑体字体来显示中文，避免中文乱码
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 设置axes.unicode_minus为False，确保负号能够正确显示，不会变成方块或其他符号
        plt.rcParams['axes.unicode_minus'] = False

        # 使用networkx库的draw函数来绘制有向图
        # self.digraph应该是一个NetworkX的有向图对象
        # with_labels=True表示绘制节点时要显示节点的标签
        # arrowstyle='->'表示边的箭头样式，这里指定为标准的箭头
        nx.draw(self.digraph, with_labels=True, arrowstyle='->')

        # 显示绘制的图形，这将会弹出一个窗口展示图形
        plt.show()

    @print_list_items
    def get_shortest_path_for_app_pages(self, start_node, end_node):
        # 使用dijkstra_path计算从start_node到end_node的最短路径上的节点
        path_nodes = nx.dijkstra_path(self.digraph, start_node, end_node)
        # 构造边的列表，从第二个节点开始到倒数第二个节点结束，每对相邻节点构成一条边
        edge_list = list(zip(path_nodes[:-1], path_nodes[1:]))
        return self.get_shortest_path_for_app_element(edge_list)

    def get_shortest_path_for_app_element(self, edge_list):
        """
        根据给定的边列表，获取应用程序元素的最短路径所包含的元素列表。

        Args:
            edge_list (list): 一个包含边的列表，代表最短路径中的边。

        Returns:
            list: 包含最短路径中所有元素的列表。
        """
        element_list = list()  # 初始化一个空列表，用于存储路径中的元素。
        for edge in edge_list:  # 遍历每一条边。
            # 获取与当前边相关的元素，并添加到element_list中。
            # 注意：这里假定self.page_element_adj.getEdges()[edge]返回的是一个元素列表。
            # 但是根据函数名和上下文，这里可能存在逻辑错误，因为通常边列表不应该直接转换为元素列表。
            # 如果self.page_element_adj是一个图结构，那么getEdges()[edge]应该返回与edge相关的边的信息，
            # 而不是路径上的元素。因此，这部分代码可能需要根据实际情况进行调整。
            element_list += (self.page_element_adj.getEdges()[edge])
            # 返回包含所有元素的列表。
        return element_list

    def compute_page_trust_score(self, page_content: str):
        # 定义属性列表，这里只包含了'text'和'id'两个属性
        attribute_list = self.config.ATTRIBUTE_LIST
        # 创建一个空字典，用于存储每个页面的信任分数
        score_dict = dict()
        # 打印self.allElemDict，用于调试或查看内容
        # print(self.allElemDict)
        # 遍历self.allElemDict中的每个页面名和对应的元素列表
        for pageName, element_list in self.allElemDict.items():
            # print(pageName, element_list )
            # 如果当前页面名还未在score_dict中，则初始化其分数为0
            if pageName not in score_dict.keys():
                score_dict[pageName] = 0
                # 遍历当前页面名下的每个元素
            for element in element_list:
                # print(element)
                # 遍历属性列表中的每个属性
                for attr in attribute_list:
                    # 打印当前元素的属性值，用于调试
                    # print(element[attr])
                    # 判断当前元素的属性值是否等于它自身（这里实际是多余的，因为任何值都等于自身）
                    # 并且属性值是否出现在传入的page_source字符串中
                    if element.get(attr) and element.get(attr) == element.get(attr) and element.get(attr) in page_content:
                        # 如果满足条件，则增加当前页面的信任分数，分数增加的值来自元素的'置信度'属性
                        # 注意：这里假设元素字典中包含'置信度'这个键，否则将会引发KeyError
                        score_dict[pageName] += element['置信度']
                        # 打印score_dict，用于调试或查看结果
        print(score_dict)
        if max(score_dict.values()) <= 30:
            # 分数小于等于30，则返回错误
            raise Exception("检测页面出错")
        # 返回分数最高的页面名
        return max(score_dict, key=lambda k: score_dict[k])


if __name__ == '__main__':
    from uiautomator2_automation_module import UiAutomator2TestDriver
    from config_module import ConfigManagerRUIBOSHI as config

    @timer
    def demo():
        # dev = UiAutomator2TestDriver('H675FIS8JJU8AMWW', '睿博士')
        G = AppFlowGraph(config)
        # G.show_directed_graph_visualization()
        print(G.page_element_adj.getPageName())
        # G.get_shortest_path_for_app_pages('首页', '添加设备')
        # G.get_shortest_path_for_app_pages('添加设备', 'AP热点配网')
        # G.get_shortest_path_for_app_pages('AP热点配网', 'WLAN')
        G.get_shortest_path_for_app_pages('首页', '蓝牙-设备连接中')
        G.get_shortest_path_for_app_pages('蓝牙-设备连接中', '设备添加成功')
    demo()