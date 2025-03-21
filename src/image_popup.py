import os
import time
import tkinter as tk
from PIL import Image, ImageTk


def show_image(image_path, display_time=5000):
    # 创建主窗口
    root = tk.Tk()
    root.title("Image Viewer")

    # 获取屏幕宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 加载图片
    pil_image = Image.open(image_path)
    photo = ImageTk.PhotoImage(pil_image)

    # 获取图片的宽度和高度
    image_width = photo.width()
    image_height = photo.height()

    # 设置窗口大小，确保窗口足够大以容纳图片
    window_width = max(400, image_width)
    window_height = max(300, image_height)
    root.geometry(f"{window_width}x{window_height}")

    # 将窗口放置在屏幕的右下角
    x_position = screen_width - window_width
    y_position = screen_height - window_height - 100
    root.geometry(f"+{x_position}+{y_position}")

    # 确保窗口获得焦点，并且始终在最前面显示
    root.attributes('-topmost', True)
    root.focus_force()  # 强制窗口获得焦点

    # 创建一个标签来显示图片
    label = tk.Label(root, image=photo)
    label.image = photo  # 保持对图片的引用，防止被垃圾回收

    # 将标签放置在窗口的右下角，并向上偏移200像素
    label.place(x=window_width - image_width, y=window_height - image_height)

    # 定义关闭窗口的函数
    def close_window():
        root.attributes('-topmost', False)  # 关闭前取消置顶
        root.destroy()

    # 使用 after 方法在指定时间后关闭窗口
    root.after(display_time, close_window)

    # 运行主循环
    root.mainloop()


def get_image_properties(image_path):
    try:
        with Image.open(image_path) as img:
            # 获取图像尺寸 (宽度, 高度)
            width, height = img.size

            # 获取图像格式 (例如: JPEG, PNG, GIF 等)
            format = img.format

            # 获取图像模式 (例如: RGB, RGBA, L 等)
            mode = img.mode

            # 获取图像信息 (可能包含一些元数据)
            info = img.info

            return {
                '尺寸': (width, height),
                '格式': format,
                '模式': mode,
                '信息': info
            }
    except Exception as e:
        print(f"无法打开或处理图像: {e}")
        return None


if __name__ == "__main__":
    # 示例调用
    image_path = r"C:\Users\Administrator\Desktop\video\test\IOTFAA-370148-NYPSC_2024_12_05_14_28_10_CH_1_imageName370148.jpg"
    properties = get_image_properties(image_path)
    print(properties)