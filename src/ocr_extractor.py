import time
import pytesseract
from PIL import Image

# 显式设置 Tesseract 路径
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'


def crop_image(image_path, left, top, right, bottom, output=False, target_width=None, target_height=None):
    """
    裁剪图像的特定区域并保存裁剪后的图像。

    :param image_path: 图像文件的路径
    :param left: 裁剪区域的左边界
    :param top: 裁剪区域的上边界
    :param right: 裁剪区域的右边界
    :param bottom: 裁剪区域的下边界
    :param output_path: 裁剪后图像的保存路径
    :return: 裁剪后的图像对象
    """
    try:
        # 读取图像
        image = Image.open(image_path)

        # 裁剪图像
        cropped_image = image.crop((left, top, right, bottom))

        # 保存裁剪后的图像
        if output:
            # 调整图像大小
            if target_width and target_height:
                cropped_image = cropped_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            cropped_image.save(image_path)

        return cropped_image
    except Exception as e:
        print(f"Error cropping image: {e}")
        return None


def extract_text_from_image(image_path, lang='chi_sim', crop_area=None):
    """
    从图像中提取文本。

    :param image_path: 图像文件的路径
    :param lang: OCR 识别的语言，默认为简体中文 ('chi_sim')
    :param crop_area: 裁剪区域的坐标 (left, top, right, bottom)，可选
    :return: 提取的文本
    """
    try:
        # 读取图像
        if crop_area:
            left, top, right, bottom = crop_area
            image = crop_image(image_path, left, top, right, bottom)
        else:
            image = Image.open(image_path)

        # 进行 OCR
        text = pytesseract.image_to_string(image, lang=lang)

        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None


if __name__ == "__main__":
    import uiautomator2_extended

    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 0.5
    app.go_to_page('登录')
    app.go_to_page('首页', '18086409233', 'cx123456789')
    time.sleep(5)
    app.go_to_page('日历', '699245')
    screenshot_path = app.save_screenshotV1()

    # 裁剪区域的坐标 (左, 上, 右, 下)
    crop_area = (0, 2010, 1080, 2080)

    # 进行 OCR
    text = extract_text_from_image(screenshot_path, lang='chi_sim', crop_area=crop_area)
    words = text.split()  # 默认以空格为分隔符
    if text:
        print("OCR Result:")
        print(words)
    else:
        print("Failed to extract text from the image.")
