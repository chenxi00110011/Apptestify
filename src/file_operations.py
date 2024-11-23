import os
import hashlib
import re
from datetime import datetime


# from my_decorator import match_pattern_in_list, print_list_items


def rename_file(old_path, new_name):
    """
    Rename a file from old_path to new_name.

    :param old_path: The current full path of the file.
    :param new_name: The new name for the file (without the path).
    """
    directory = os.path.dirname(old_path)
    new_path = os.path.join(directory, new_name)

    try:
        os.rename(old_path, new_path)
        print(f"The file has been renamed from '{old_path}' to '{new_path}'.")
    except OSError as e:
        print(f"Error renaming file: {e}")


# @print_list_items
# @match_pattern_in_list(r'\d{3,}')
def list_files(directory, extension=None):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if extension is None or extension in file:
                file_list.append(file)
    return file_list


def get_file_md5(file_path):
    # 创建一个md5对象
    md5_hash = hashlib.md5()

    # 打开文件并逐块读取
    with open(file_path, 'rb') as f:
        # 循环读取文件块
        for chunk in iter(lambda: f.read(4096), b""):
            # 更新md5对象
            md5_hash.update(chunk)

    # 返回文件的md5哈希值
    return md5_hash.hexdigest()


# 定义一个函数来提取日期并转换为时间戳
def parse_log_entry(entry, date_pattern):
    # 使用正则表达式匹配日期时间
    match = re.search(date_pattern, entry)
    if match:
        date_str = match.group(0)

        # 解析日期时间字符串
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

        # 转换为时间戳
        timestamp = dt.timestamp()

        return timestamp
    else:
        return None


if __name__ == '__main__':
    date_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
    print(parse_log_entry("[AI IPC]2024-11-15 16:36:17有一个[移动侦测]事件", date_pattern))
