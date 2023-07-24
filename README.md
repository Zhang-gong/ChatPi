# ChatPi

ChatPi是一款以树莓派作为媒介的智能音响。通过调用百度API来实现语音转文字/文字转语音，调用ChatGPT回答问题。

Attention:由于国内的网络无法直连OpenAI，所以需要使用智能代理。我的方法是手机设为热点，并在手机上下载开启everyproxy，把树莓派的流量转发至智能代理端口（一定得是智能代理，全局代理就用不了百度的API了）。
## Bill of Materials

- 1 x Raspberry Pi 
- 1 x USB microphone 
- 1 x Speaker


## quick start

```
sudo apt-get install mpg123
sudo apt-get install pulseaudio 
pulseaudio --start
```

接下来启动项目:

```
python3 chatbot.py [--model <model_path>] [--duration [seconds]]

```

参数`model_path`填入模型路径,模型放在文件夹`snowboy/resources/models/`中,默认为`snowboy/resources/models/ChatPi.pmdl`

参数`duration`为问题的持续时间,也就是录音时长,默认为`5`，单位秒

也可以输入`--help`查看参数说明

启动程序后就进入了运行状态，请对麦克风说"ChatPi"(ChatPi是默认唤醒词,如果你
有自己设置的唤醒词,请使用自己的唤醒词)，唤醒服务.听到"ding"的一声后,请在倒计时结束前说出你的问题.

音频重采样后将发送到百度语音转文字,再将文字发送给OpenAI.OpneAI的响应再被发送给百度文字转语音,自动播放文件.

可以在chatbot.py的conversation_list里设置预设.

## train your own wake-up-model
snowboy停止API服务了:
https://github.com/wzpan/wukong-robot/issues/139

训练自己的唤醒词:
https://snowboy.hahack.com/

## 项目汇报及演示视频

https://www.bilibili.com/video/BV1KX4y1i7GH
