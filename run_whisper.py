import openai
import openai
import whisper
from whisper.utils import get_writer
import sys 
sys.path.append('.')
import openai 
from pathlib import Path 
import subprocess

'''
需要翻墙
install openai-whisper
install openai
目前有两种方式，1) 是远程调用openai的whisper服务识别, 2)是用本地的whisper模型识别。
目前使用的是方式1识别
注释的三行代码，是使用方式2识别的，本地numpy有问题，还在debug
'''

openai.api_key = ""
#model = whisper.load_model("medium")



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

    # audio_file= open(media_path, "rb")
    # transcript = model.transcribe(audio_file)

    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)
    srt_writer = get_writer("srt", output_directory)
    srt_writer(transcript, media_path)

gen_subtitles('gpt4audio.mp4', output_directory='./subtitles')