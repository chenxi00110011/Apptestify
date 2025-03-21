from moviepy import VideoFileClip


def get_video_properties(file_path):
    """
    使用 moviepy 解析视频文件的基本属性。

    参数:
    file_path (str): 视频文件的路径。

    返回:
    dict: 包含视频属性的字典，如分辨率、帧率、时长等。
    """
    with VideoFileClip(file_path) as clip:
        properties = {
            'duration': clip.duration,  # 视频时长 (秒)
            'resolution': clip.size,  # 分辨率 (宽度, 高度)
            'fps': clip.fps,  # 帧率 (每秒帧数)
            # 'bitrate': clip.bitrate,  # 比特率 (moviepy 不提供此属性)
            # 'codec': clip.reader.infos['video_codec'] if 'video_codec' in clip.reader.infos else None
        }
        return properties


# 示例调用
if __name__ == "__main__":
    file_path = r"C:\Users\Administrator\Desktop\video\videos\IOTFAA-288577-SZLTM_2024_12_05_16_55_45_CH_1_deviceName288577.mp4"
    properties = get_video_properties(file_path)
    for key, value in properties.items():
        print(f"{key}: {value}")