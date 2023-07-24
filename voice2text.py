# -*- coding:utf-8 -*-
from aip import AipSpeech

APP_ID = '3*****3'
API_KEY = 'f7***************a'
SECRET_KEY = 'pw******************AaXG3'


client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#以下是读取录音文件返回文字的方法
# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件，并返回识别结果
my_file = 'recording_2.wav'
result = client.asr(get_file_content(my_file), 'pcm', 16000, { 'dev_pid': 1536,})
print(result)

# #以下是读取文本，返回audio.mp3文件的方法
# result  = client.synthesis('你好百度', 'zh', 1, {
#     'vol': 5,
# })
#
# # 识别正确返回语音二进制
# if not isinstance(result, dict):
#     with open('auido.mp3', 'wb') as f:
#         f.write(result)
