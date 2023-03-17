## 目的
using openai whisper for speech 2 text applications

如果输入路径是MP3格式，会直接交给openai模型识别

如果输入路径是mp4格式，代码会用ffmpeg转成mp3识别

## 需要翻墙

## 安装
安装ffmpeg

pip install openai-whisper

pip install openai

## 简单描述
目前有两种方式，1) 是远程调用openai的whisper服务识别, 2)是用本地的whisper模型识别。

目前使用的是方式1识别, 因为这种方式需要远程call openai，**需要翻墙**

注释的三行代码，是使用方式2识别的，本地numpy有问题，还在debug

## code
```python
import openai
import openai
import whisper
from whisper.utils import get_writer
import sys 
sys.path.append('.')
import openai 
from pathlib import Path 
import subprocess
import os 

'''
需要翻墙
install openai-whisper
install openai
目前有两种方式，1) 是远程调用openai的whisper服务识别, 2)是用本地的whisper模型识别。
目前使用的是方式1识别
注释的三行代码，是使用方式2识别的，本地numpy有问题，还在debug
'''

openai.api_key = ""
MODE = 'local'
output_dir = 'subtitles'


if MODE == 'local':  #是用本地的whisper模型识别。tiny,base,medium,large
    model = whisper.load_model("base")
elif MODE == 'remote':  #是远程调用openai的whisper服务识别, 
    if not openai.api_key:
        raise 'OPEN API KEY needed for remote call'
    pass


def extract_audio(video_path, output_path, force=True):
    output_path = str(output_path)
    if not force and os.path.exists(output_path):
        return
    
    cmd = f'ffmpeg -i {video_path} -vn -acodec copy {output_path}'
    subprocess.run(cmd, shell=True)

def gen_subtitles(media_path, output_directory):
    if media_path.startswith('.mp4'):
        audio_path = Path(media_path).with_suffix('.mp3')
        extract_audio(media_path, audio_path)
    else:
        audio_path = media_path
    audio_file= open(media_path, "rb")

    if MODE == 'local':
        transcript = model.transcribe(media_path)
    elif MODE == 'remote':
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    
    print(transcript)
    srt_writer = get_writer("srt", output_directory)
    srt_writer(transcript, media_path)


os.makedirs(output_dir, exist_ok=True)
gen_subtitles('gpt4audio.mp4', output_directory=output_dir)
```
