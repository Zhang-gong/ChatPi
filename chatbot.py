# -*- coding:utf-8 -*-
"""
Created on  # 19:28  19:28
@author: Gong Zhang
"""
import sys
import subprocess
import pyaudio
import wave
import openai
from snowboy import snowboydecoder
import signal
import requests
from Text2Voice import text2voice
from tools import options_func

CHUNK = 1024  # 每次读取的音频数据大小
FORMAT = pyaudio.paInt16  # 音频数据格式为16位整数
CHANNELS = 1  # 单声道
RATE = 48000  # 采样率（每秒采样点数）
TARGET_RATE = 16000
RECORD_SECONDS = 5  # 录制时长
WAVE_OUTPUT_FILENAME = "recording.wav"  # 保存音频的文件名
FINAL_OUTPUT_FILENAME= "recording_16000.wav"
MAX_CONVERSATION= 3 #对话轮数
from aip import AipSpeech

""" 你的 BAIDU APPID AK SK """
BD_APP_ID = '3*****3'
BD_API_KEY = 'f7***************a'
BD_SECRET_KEY = 'pw******************AaXG3'

"""openAI API"""
openai.api_key = "sk-ss8r***************************V0H0X"

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

def mic(record_seconds):
    p = pyaudio.PyAudio()
    # 打开麦克风输入流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    stream.volume = 1
    print("开始录制音频...")

    frames = []  # 用于存储音频帧数据

    # 读取音频数据并保存
    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录制完成！")

    # 停止录制并关闭流
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 保存音频文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("音频保存为：" + WAVE_OUTPUT_FILENAME)
    #播放音频
    #os.system("aplay recording.wav")

def changeRate():
    # 使用FFmpeg降低采样频率
    command = [
        "ffmpeg",
        "-i", WAVE_OUTPUT_FILENAME,
        "-ar", str(TARGET_RATE),
        FINAL_OUTPUT_FILENAME
    ]

    # 运行命令行
    subprocess.run(command, check=True)

    print("音频采样频率已降低为", TARGET_RATE)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def voice2Text():
    #根据语音调用百度的API获取文字
    client = AipSpeech(BD_APP_ID, BD_API_KEY, BD_SECRET_KEY)
    response = client.asr(get_file_content(FINAL_OUTPUT_FILENAME), 'pcm', 16000, {'dev_pid': 1536, })
    print(response)
    result = response['result'][0]
    print(result)
    return result

def chatGPT(conversation_list):
    # 设置 OpenAI API 的代理
    proxies = {
        "http": "http://192.168.43.1:55562",
        "https": "http://192.168.43.1:55562"
    }
    headers = {
        "Authorization": "Bearer "+openai.api_key,
        "Content-Type": "application/json"
    }
    data = {
        "messages": conversation_list,
        "model": "gpt-3.5-turbo"
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, proxies=proxies)
    completion = response.json()
    print(completion)
    answer = completion["choices"][0]["message"]["content"]
    return answer



def play(save_file):
    command = [
        "aplay",
        save_file
    ]

    # 运行命令行
    subprocess.run(command, check=True)

def deleteAudio(save_file):
    command = [
        "rm",
        WAVE_OUTPUT_FILENAME,
        FINAL_OUTPUT_FILENAME,
        save_file
    ]
    subprocess.run(command, check=True)

def show_conversation(conversation_list):
    for msg in conversation_list:
        if msg['role'] == 'user':
            print(f"\U0001f47b: {msg['content']}\n")
        else:
            print(f"\U0001f47D: {msg['content']}\n")

def chat_bot_main(duration,conversation_list = []):
    record_seconds=duration
    mic(record_seconds)
    changeRate()
    question=voice2Text()
    conversation_list.append({"role":"user","content":question})
    answer=chatGPT(conversation_list)
    #print(answer)
    conversation_list.append({"role": "assistant", "content": answer})
    show_conversation(conversation_list)
    save_file=text2voice(answer)
    play(save_file)
    deleteAudio(save_file)
    if len(conversation_list) > 2 * MAX_CONVERSATION:
        # 删除前两个元素
        del conversation_list[:2]
        # 添加两个新元素

if __name__ == '__main__':
    opt, args = options_func()
    signal.signal(signal.SIGINT, signal_handler)
    print('Listening... Press Ctrl+C to exit')
    conversation_list = [{"role": "system", "content": "你现在正在扮演我的导师，是人工智能领域的专家，哈佛大学的教授。请你时时刻刻表现出对我的严厉要求，并且时常要斥责我使我上进。"}]
    #conversation_list = [] #无预设
    #conversation_list = [{"role": "system",
     #                     "content": "你现在正在扮演我的助理,请你表现的活跃友善。"}]
    while (not interrupted):
        detector = snowboydecoder.HotwordDetector(opt.model, sensitivity=0.5)

        def detected_callback():
            """ start chatpi service"""
            # detector.terminate()
            # chatbot.chat_bot_main()
            play("snowboy/resources/ding.wav")
            print("---------start ChatPi---------")
            detector.terminate()
            chat_bot_main(opt.duration,conversation_list)
        detector.start(detected_callback, interrupt_check=interrupt_callback,
                       sleep_time=0.03)
        detector.terminate()




