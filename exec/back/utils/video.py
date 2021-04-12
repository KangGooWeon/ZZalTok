import os
import platform
from collections import OrderedDict

import urllib.request
import zipfile
import ffmpy
import stat

from config import config

FFMPEG_FILENAME = "ffmpeg"
FFMPEG_ZIP = FFMPEG_FILENAME + ".zip"

# ffmpeg 파일 다운로드
if not os.path.isdir(config.ffmpeg_path):
    urllib.request.urlretrieve(
        "http://kumoh.synology.me/ffmpeg.zip",  # NOSONAR
        filename=os.path.join(config.root, FFMPEG_ZIP))
    with zipfile.ZipFile(os.path.join(config.root, FFMPEG_ZIP), "r") as zip_ref:
        os.makedirs(config.ffmpeg_path, exist_ok=True)
        zip_ref.extractall(config.ffmpeg_path)
    if platform.system() == "Windows":  # 윈도우인 경우 linux 실행 파일을 삭제
        os.remove(os.path.join(config.ffmpeg_path, FFMPEG_FILENAME))
    else:  # 리눅스인 경우 윈도우 파일을 삭제하고, 실행 권한 추가
        os.remove(os.path.join(config.ffmpeg_path, FFMPEG_FILENAME + ".exe"))
        st = os.stat(os.path.join(config.ffmpeg_path, FFMPEG_FILENAME))
        os.chmod(os.path.join(config.ffmpeg_path, FFMPEG_FILENAME), st.st_mode | stat.S_IEXEC)

# ffmpeg를 환경변수 PATH에 추가
os.environ["PATH"] += os.pathsep + config.ffmpeg_path


def convert3x_faster_video(input_path: str, output_path: str):
    # !ffmpeg -i original.mp4 -r 60 -vf "setpts=(PTS-STARTPTS)/3" 3x.mp4
    ffmpy.FFmpeg(
        inputs={input_path: None},
        outputs={output_path: '-r 60 -vf "setpts=(PTS-STARTPTS)/3"'},
        global_options=['-y']
    ).run()


def insert_audio_on_video(input_video_path: str, input_audio_path: str, output_path: str):
    # !ffmpeg -i 3x.mp4 -i bakamitai_template.mp3 -map 0:v -map 1:a -c:v copy -shortest complete.mp4
    ffmpy.FFmpeg(
        inputs=OrderedDict([(input_video_path, None), (input_audio_path, None)]),
        outputs={output_path: '-map 0:v -map 1:a -c:v copy -shortest'},
        global_options=['-y']
    ).run()


def insert_audio_on_video_fps30(input_video_path: str, input_audio_path: str, output_path: str):
    # !ffmpeg -i 3x.mp4 -i bakamitai_template.mp3 -map 0:v -map 1:a -c:v copy -shortest complete.mp4
    ffmpy.FFmpeg(
        inputs=OrderedDict([(input_video_path, '-r 30'), (input_audio_path, None)]),
        outputs={output_path: '-map 0:v -map 1:a -c:v libx264 -shortest'},
        global_options=['-y']
    ).run()


def create_video_thumbnail(input_video_path, output_image_path):
    if os.path.splitext(output_image_path)[-1].lower() != '.png':
        raise Exception('Only png files are allowed for output')  # NOSONAR
    # !ffmpeg.exe -i twice.mp4 -vcodec png -vframes 1 -vf thumbnail=100 result.png
    ffmpy.FFmpeg(
        inputs={input_video_path: None},
        outputs={output_image_path: "-vcodec png -vframes 1 -vf thumbnail=100"},
        global_options=['-y']
    ).run()
