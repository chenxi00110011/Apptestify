import os
import re
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


if __name__ == '__main__':
    # Example usage:
    file_list = list_files(r"C:\Users\Administrator\Desktop\g固件包\easydebug\Sessions", "RELAY")
    print(sorted(file_list, key=str))
