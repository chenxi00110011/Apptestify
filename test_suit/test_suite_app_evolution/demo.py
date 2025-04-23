import time

from image_popup import show_image
from pygame import mixer
import time


def play_mp3(mp3_path):
	try:
		# 初始化混音器
		mixer.init()
		
		# 加载 MP3 文件
		mixer.music.load(mp3_path)
		
		# 播放音乐
		mixer.music.play()
		
		# 等待音乐播放完成（假设音乐时长为 30 秒）
		time.sleep(30)
		
		# 停止音乐（如果需要）
		mixer.music.stop()
	except Exception as e:
		print(f"播放 MP3 文件时出错: {e}")


# 调用函数

for i in range(10):
	image_path = r"C:\Users\Administrator\P2pServerTest\Apptestify\data\video\VCG211374260806.jpg"
	show_image(image_path)
	
	time.sleep(10)
	
	# 播放 MP3 文件
	mp3_path = r"C:\Users\Administrator\P2pServerTest\Apptestify\data\video\hrxz.com-1cccmyrjxy146727.mp3"
	play_mp3(mp3_path)
	
	time.sleep(120)
