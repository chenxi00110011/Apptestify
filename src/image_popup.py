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


if __name__ == "__main__":
    # 指定图片路径和显示时间
    image_path = r"C:\Users\Administrator\Desktop\video\截图\H675FIS8JJU8AMWW\XXX\2024-11-22\test.jpg"
    display_time = 10000  # 显示时间为10秒
    show_image(image_path, display_time)
