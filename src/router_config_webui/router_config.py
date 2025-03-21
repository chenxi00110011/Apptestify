import time
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def configure_browser():
    # 配置 Chrome 选项
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    # 初始化 Chrome 浏览器
    driver = webdriver.Chrome(options=options)
    return driver


def browser():
    # 初始化 Chrome 浏览器
    driver = webdriver.Chrome()
    return driver


def read_config(file_path):
    # 读取INI文件
    _config = configparser.ConfigParser()
    _config.read(file_path, encoding="utf-8")
    return _config


def get_sections(file_path):
    # 读取INI文件
    _config = configparser.ConfigParser()
    _config.read(file_path, encoding="utf-8")

    # 返回所有段名
    return _config.sections()


def get_value(file_path, _section, key):
    # 读取INI文件
    _config = configparser.ConfigParser()
    _config.read(file_path, encoding="utf-8")

    # 返回对应的value
    return _config.get(_section, key)


def is_element_present(driver, by, value, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return True
    except (TimeoutException, NoSuchElementException):
        return False


def router_management(url: str, login_pwd: str, ssid: str, pwd: str) -> None:
    # 初始化浏览器
    driver = configure_browser()

    try:
        # 打开路由器管理界面
        driver.get(url)
        time.sleep(1.0)

        # 判断登录密码输入框是否存在
        if not is_element_present(driver, By.ID, "lgPwd"):
            print("Login password input field not found.")
            return

        # 查找密码输入框
        password_input = driver.find_element(By.ID, "lgPwd")

        # 输入密码
        password_input.send_keys(login_pwd)

        # 点击确认
        login_button = driver.find_element(By.ID, "loginSub")
        login_button.click()

        # 等待登录后页面加载完成
        if not is_element_present(driver, By.ID, "hostWifiNameBs"):
            print("SSID input field not found after login.")
            return

        # 输入SSID和密码
        ssid_input = driver.find_element(By.ID, "hostWifiNameBs")
        pwd_input = driver.find_element(By.ID, "hostWifiPwdBs")
        save_button = driver.find_element(By.ID, "hostWifiSaveBs")
        ssid_input.clear()
        pwd_input.clear()
        ssid_input.send_keys(ssid)
        pwd_input.send_keys(pwd)
        save_button.click()

        # 等待保存后页面加载完成
        if not is_element_present(driver, By.XPATH, "//input[@type='button' and @value='确 定']"):
            print("Confirm button not found after saving.")
            return

        # 二次确认
        confirm_button = driver.find_element(By.XPATH, "//input[@type='button' and @value='确 定']")
        confirm_button.click()
        time.sleep(1.0)

    finally:
        # 关闭浏览器
        driver.quit()


def modify_wifi(_config_path: str, _section: str):
    # 读取配置
    config = read_config(_config_path)
    url = config.get(_section, "url")
    login_password = config.get(_section, "login_password")
    ssid = config.get(_section, "ssid")
    pwd = config.get(_section, "wifi_password")

    # 执行管理操作
    router_management(url, login_password, ssid, pwd)


if __name__ == "__main__":
    # 配置文件路径
    config_path = r'C:\Users\Administrator\P2pServerTest\Apptestify\config\router.ini'
    section = "英文标点符号"
    config = read_config(config_path)
    print(config.get(section, "ssid"))
    modify_wifi(config_path, section)
