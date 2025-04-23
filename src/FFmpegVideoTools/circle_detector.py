# -*- coding: utf-8 -*-
"""
Author: chen xi
Date: 2025/4/21 下午1:50
File: circle_detector.py
"""

import cv2
import numpy as np
import os


def detect_circles(image_path):
    # 检查文件是否存在
    if not os.path.exists(image_path):
        print(f"文件不存在: {image_path}")
        return []

    # 尝试读取图片
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图片文件: {image_path}")
        return []

    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 高斯模糊以减少噪声
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # 使用霍夫圆变换检测圆形
    circles = cv2.HoughCircles(
        gray_blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=50,
        param2=30,
        minRadius=10,
        maxRadius=100
    )

    # 初始化一个列表存储圆形的信息（中心坐标、颜色、直径）
    circle_info = []

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            center = (circle[0], circle[1])  # 圆心坐标 (x, y)
            radius = circle[2]              # 半径
            diameter = 2 * radius           # 直径

            # 提取圆心位置的颜色（BGR 格式）
            color = image[center[1], center[0]].tolist()  # 获取 BGR 颜色值

            # 存储圆形信息
            circle_info.append({
                "center": center,       # 圆心坐标
                "color": color,         # 圆心处的颜色（BGR 格式）
                "diameter": diameter    # 圆的直径
            })

    return circle_info


# 测试代码
if __name__ == "__main__":
    image_path = r"C:\Users\Administrator\Desktop\c.jpg"
    circles = detect_circles(image_path)
    if circles:
        print("检测到的圆形信息：")
        for idx, circle in enumerate(circles):
            print(circles)
    else:
        print("未检测到圆形。")