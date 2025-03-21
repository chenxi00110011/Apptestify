# test_live.py
import os.path
import time
import pytest
import uiautomator2_extended
from FFmpegVideoTools.video_metadata_extractor import get_video_properties
from adb_commands import AdbManager
from file_operations import get_all_file_paths, remove_directory_recursively
from image_popup import get_image_properties
from router_config import modify_wifi, read_config, router_management, get_sections

_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [
    # 国内手机账户转让设备
    (account_config.get('睿博士正式服账号', '中国手机账户_1'),
     account_config.get('睿博士正式服账号', '中国手机密码_1'),
     _config.get('单目设备', 'did_1'),
     _config.get('单目设备', 'name_1'),
     account_config.get('睿博士正式服账号', '中国区号'),
     account_config.get('睿博士APP', 'rui_screenshot'),
     account_config.get('睿博士APP', 'pc_dir')
     )
]


@pytest.mark.repeat(1)
@pytest.mark.case_name("单目IPC切换画质后截图")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.live
@pytest.mark.parametrize("account, pwd, did, name, areaCode, rui_screenshot, pc_dir", parameter)
def test_switch_quality_and_snapshot(account, pwd, did, name, areaCode, rui_screenshot, pc_dir):
    # 打开app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('登录')
    if not app.exists_element(selector="text", value="+86"):
        app.go_to_page("选择国家", areaCode)
    app.go_to_page('首页', account, pwd)
    app.go_to_page('直播', name)

    # 切换画质并截图
    quality_dict = {"超清": (2880, 1624), "高清": (640, 360), "标清": (640, 360)}
    app.driver(text="画质").click()
    for quality, resolution in quality_dict.items():
        time.sleep(1)
        app.driver(text=quality).click()
        time.sleep(5)
        app.driver(text="截图").click()
        time.sleep(5)

        # 下载截图文件
        AdbManager.pull_file('H675FIS8JJU8AMWW', rui_screenshot, pc_dir)

        # 获取图片路径
        dir_path = os.path.join(pc_dir, 'screenshot')
        file_path = get_all_file_paths(dir_path)[0]

        # 解析图片,检查画质对应的分辨率
        properties = get_image_properties(file_path)
        assert properties.get('尺寸') == resolution

        # 删除目录
        remove_directory_recursively(dir_path)

        # 清空睿博士的截图
        os.system("adb shell rm /sdcard/Pictures/P6SLite/screenshot/*")


_config = read_config(r'..\..\config\device_info.ini')
account_config = read_config(r'..\..\config\base.ini')
parameter = [
    # 国内手机账户转让设备
    (account_config.get('睿博士正式服账号', '中国手机账户_1'),
     account_config.get('睿博士正式服账号', '中国手机密码_1'),
     _config.get('单目设备', 'did_1'),
     _config.get('单目设备', 'name_1'),
     account_config.get('睿博士正式服账号', '中国区号'),
     account_config.get('睿博士APP', 'rui_videos'),
     account_config.get('睿博士APP', 'pc_dir')
     )
]


@pytest.mark.repeat(1)
@pytest.mark.case_name("单目IPC切换画质后录像")
# @pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.live_test
@pytest.mark.parametrize("account, pwd, did, name, areaCode, rui_videos, pc_dir", parameter)
def test_switch_quality_and_start_recording(account, pwd, did, name, areaCode, rui_videos, pc_dir):
    # 打开app
    app = uiautomator2_extended.Uiautomator2SophisticatedExecutor('H675FIS8JJU8AMWW', '睿博士')
    time.sleep(15)
    app.run_parameters['rectangle'] = 1.0
    app.go_to_page('登录')
    if not app.exists_element(selector="text", value="+86"):
        app.go_to_page("选择国家", areaCode)
    app.go_to_page('首页', account, pwd)
    app.go_to_page('直播', name)

    # 切换画质并截图
    quality_dict = {"超清": {"duration": 30, "resolution": [2304, 1296], "fps": 15},
                    "高清": {"duration": 30, "resolution": [640, 360], "fps": 15},
                    "标清": {"duration": 30, "resolution": [640, 360], "fps": 12}}
    for quality, resolution in quality_dict.items():
        # 删除目录
        dir_path = os.path.join(pc_dir, 'videos')
        remove_directory_recursively(dir_path)

        # 清空睿博士的截图
        os.system(f"adb shell rm {rui_videos}*")

        if not app.exists_element(selector="text", value="超清"):
            app.driver(text="画质").click()
            time.sleep(1)
        app.driver(text=quality).click()
        time.sleep(5)
        app.driver(text="录像").click()
        time.sleep(30)
        app.driver(text="录像").click()
        time.sleep(5)

        # 下载录像文件
        AdbManager.pull_file('H675FIS8JJU8AMWW', rui_videos, pc_dir)

        # 获取录像路径
        file_path = get_all_file_paths(dir_path)[0]

        # 解析图片,检查画质对应的分辨率
        properties = get_video_properties(file_path)
        print(properties)
        assert abs(properties.get('duration') - resolution.get('duration')) < 3
        assert properties.get('resolution') == resolution.get('resolution')
        assert abs(properties.get('fps') - resolution.get('fps')) < 0.2
