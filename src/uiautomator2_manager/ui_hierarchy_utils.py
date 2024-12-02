import uiautomator2 as u2
from lxml import etree

# 连接到设备
d = u2.connect()


# 定义一个函数来查找元素
def find_elements(root, text):
    elems = []
    for elem in root.iter():
        if 'text' in elem.attrib and elem.attrib['text'] == text:
            elems.append(elem)

    return elems


# 定义一个函数来获取元素的路径
def get_element_path(element):
    path = []
    while element is not None:
        path.append(element)
        element = element.getparent()
    return path[::-1]  # 反转路径以从根到叶


# 定义一个函数来计算两个节点之间的层级差
def calculate_level_difference(element1, element2):
    path1 = get_element_path(element1)
    path2 = get_element_path(element2)

    # 找到共同的祖先节点
    common_ancestor = None
    for e1, e2 in zip(path1, path2):
        if e1 == e2:
            common_ancestor = e1
        else:
            break

    # 计算层级差
    if common_ancestor is not None:
        level_diff = (len(path1) - 1 - path1.index(common_ancestor)) + (len(path2) - 1 - path2.index(common_ancestor))
        return level_diff
    else:
        return -1  # 如果没有共同祖先节点，返回-1表示无法计算层级差


def get_level_differences(d, element1_text, element2_text):
    """获取指定文本的两个元素之间的层级差列表"""
    # 获取当前屏幕的层次结构
    hierarchy = d.dump_hierarchy()

    # 将字符串转换为字节
    hierarchy_bytes = hierarchy.encode('utf-8')

    # 解析 XML
    root = etree.fromstring(hierarchy_bytes)

    # 查找第一个元素
    elements1 = find_elements(root, element1_text)
    if not elements1:
        print(f"未能找到包含文本 '{element1_text}' 的元素")
        return []

    # 查找第二个元素
    elements2 = find_elements(root, element2_text)
    if not elements2:
        print(f"未能找到包含文本 '{element2_text}' 的元素")
        return []

    # 计算层级差
    level_diffs = []
    for element1 in elements1:
        for element2 in elements2:
            level_diff = calculate_level_difference(element1, element2)
            if level_diff != -1:
                level_diffs.append(level_diff)
            else:
                print("无法计算两个节点之间的层级差（没有共同的祖先节点）")
    # 返回层级最小元素的下标
    return level_diffs.index(min(level_diffs))


if __name__ == "__main__":

    element1_text = "000086"
    element2_text = "消息"

    level_diffs = get_level_differences(d, element1_text, element2_text)

    if level_diffs is not None:
        print(f"下标为 {level_diffs}的元素")
    else:
        print("没有找到有效的层级差")
