# -*- coding: utf-8 -*-
"""
-
Author:
Date:2024年3月30日
"""

# -*- coding: utf-8 -*-
import pandas as pd


class AdjacencyListHandler:
    data_type = {'text': str, 'resource-id': str, '置信度': int}

    def __init__(self, file_path, sheetName):
        self.file_path = file_path
        self.sheetName = sheetName
        # print(self.file_path,self.sheetName)
        self.dataFrame = self.getDateFrame()
        self.AL_dataFrame = self.filter_adjacent_vertices()

    # 获取excel数据
    def getDateFrame(self) -> dict:

        df = pd.read_excel(self.file_path, sheet_name=self.sheetName, dtype=self.data_type)
        # 重置索引，不保留原来的索引列
        df_reset = df.reset_index(drop=True)
        # 过滤掉以'Unnamed:'开头的列
        df_filtered = df_reset.loc[:, ~df.columns.str.startswith('Unnamed:')]
        return df_filtered

    # 删选非空的第二列，返回邻接表
    def filter_adjacent_vertices(self):
        second_column = self.dataFrame.iloc[:, 1]  # 获取第二列的数据
        non_null_rows = second_column.notnull()  # 检查第二列哪些行是非空的
        df = self.dataFrame[non_null_rows]
        # 重置索引，不保留原来的索引列
        df_reset = df.reset_index(drop=True)
        # 过滤掉以'Unnamed:'开头的列
        df_filtered = df_reset.loc[:, ~df.columns.str.startswith('Unnamed:')]
        # print(df_filtered)
        return df_filtered

    # 获取邻接表的页面节点
    def getPageName(self) -> set:
        first_column_data = self.dataFrame.iloc[:, 0]  # 获取第一列的数据
        first_column_set = set(first_column_data)  # 将第一列的数据转换为一个集合
        return first_column_set

    # 获取邻接表的边
    def getEdges(self) -> dict:
        edges = dict()
        df = self.AL_dataFrame
        AL_list = df.to_dict('records')
        # print(len(AL_list))
        # 直接迭代DataFrame的行，这样可以避免创建row_numbers列表
        for index, row in df.iterrows():
            # print(index)
            # 使用iloc或loc直接访问值，这样更有效率
            value1 = row.iloc[0]  # 或者使用 row[headers_list[0]] 如果列名已知
            value2 = row.iloc[1]  # 或者使用 row[headers_list[1]]
            # 检查两个值都不是None
            if value2 is not None and value1 is not None:
                key = (value1, value2)
                if key not in edges.keys():
                    edges[key] = []
                    edges[key].append(AL_list[index])
                else:
                    edges[key].append(AL_list[index])
                # edges[key] = df.to_dict('records')  # 或者可以设置为其他有意义的值，例如边的权重
        # print(edges)
        return edges

    def read_all_elements_from_excel(self) -> dict:
        """
        从Excel文件中读取所有元素，并将它们组织成一个嵌套字典结构。
        外层字典的键是页面名称，内层字典的键是属性名称，值是对应的属性值。

        :return: 返回一个嵌套字典，结构如下：
                {
                    '页面名称1': {'属性1': 值1, '属性2': 值2, ...},
                    '页面名称2': {'属性1': 值3, '属性2': 值4, ...},
                    ...
                }
        """
        # 创建一个空字典用于按页面名称组织元素
        page_elements_dict = dict()
        # 假设self.dataFrame是已经加载的pandas DataFrame对象
        df = self.dataFrame
        # 将DataFrame转换为记录列表（每行是一个字典）
        AL_list = df.to_dict('records')

        # 遍历DataFrame的每一行
        for index, row in df.iterrows():
            # 获取当前行的第一个元素作为页面名称
            page_name = row.iloc[0]
            # 如果页面名称为空，则跳过当前行
            if not page_name:
                continue
                # 如果页面名称不在page_elements_dict的键中，则添加一个新的键，并初始化其值为一个包含当前行字典的列表
            if page_name not in page_elements_dict:
                page_elements_dict[page_name] = [AL_list[index]]
                # 如果页面名称已经在page_elements_dict中，则将当前行字典添加到对应的列表中
            else:
                page_elements_dict[page_name].append(AL_list[index])

                # 返回组织好的嵌套字典
        return page_elements_dict


def write_element_to_excel(new_data, file_path, sheet_name):
    # 读取原有的Excel文件
    existing_df = pd.read_excel(file_path, sheet_name=sheet_name)
    # # 将新数据转换为DataFrame
    # new_df = pd.DataFrame(new_data)
    # 将新数据追加到原有的DataFrame中
    combined_df = pd.concat([existing_df, new_data], ignore_index=True)
    # 将合并后的DataFrame写回Excel文件，覆盖原有数据
    combined_df.to_excel(file_path, sheet_name=sheet_name, index=False)


def pad_dict_values_to_max_length(d, fill_value=None):
    # 找出字典中所有列表的最大长度
    max_length = max(len(value) for value in d.values())
    # 创建一个新字典，用于存储补齐后的键值对
    padded_dict = {}
    # 遍历原始字典的键值对
    for key, value in d.items():
        # 如果当前列表长度小于最大长度，则使用填充值进行补齐
        padded_value = value + [fill_value] * (max_length - len(value))
        # 将补齐后的列表添加到新字典中
        padded_dict[key] = padded_value
    return padded_dict


def filter_df_and_write_excel(df: dict, filter_column: str, filter_value: str, output_file: str, sheet_name: str):
    """
    筛选DataFrame中指定列的值等于filter_value的行，并将结果写入Excel文件。
    参数:
    df (pandas.DataFrame): 要筛选的DataFrame。
    filter_column (str): 要筛选的列名。
    filter_value (Any): 用于筛选的值。
    output_file (str): 输出Excel文件的路径。
    返回:
    None
    """
    df = pd.DataFrame(df)
    # 筛选DataFrame
    filtered_df = df.loc[df[filter_column] != filter_value]
    # 将筛选后的DataFrame写入Excel文件
    write_element_to_excel(filtered_df, output_file, sheet_name=sheet_name)


if __name__ == '__main__':
    # al = AdjacencyListHandler(conf.PAGE_ELEMENT_FILE_PATH, conf.ADJACENCY_LIST)
    # # print(al.AL_dataFrame.to_dict('records'))
    # # print(al.AL_dataFrame.columns)
    # # print(al.getPageName())
    # # d = al.getEdges()
    # # print(d[('登录页', '首页')])
    # print(al.read_all_elements_from_excel()['登录页'])
    # 创建一个简单的DataFrame
    pass
