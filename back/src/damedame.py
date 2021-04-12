import os
import git
import urllib.request
import zipfile
from config import config
from utils import video

if not os.path.isdir(config.first_order_model_path):
    print("다메다메 프로젝트 클론 중", end=' ')
    git.Repo.clone_from("https://github.com/AliaksandrSiarohin/first-order-model", config.first_order_model_path)
    print("done")

if not os.path.isdir(config.dame_path):
    print("다메다메 학습 모델 및 템플릿 다운로드 중 - 오래 걸림", end=' ')
    urllib.request.urlretrieve(
        "https://github.com/KeepSOBP/dame/releases/download/damesource/damesource.zip" # NOSONAR
        , filename=os.path.join(config.root, "damesource.zip"))  # NOSONAR
    with zipfile.ZipFile(os.path.join(config.root, "damesource.zip"), "r") as zip_ref:  # NOSONAR
        zip_ref.extractall(config.dame_path)
    os.remove(os.path.join(config.root, "damesource.zip"))  # NOSONAR
    print("done")

if not os.path.exists(os.path.join(config.dame_path, "bakamitai_template.mp3")):  # NOSONAR
    print("다메다메 오디오 리소스 다운로드 중", end=' ')
    urllib.request.urlretrieve(
        "https://github.com/KeepSOBP/dame/releases/download/damesource/bakamitai_template.mp3"
        , filename=os.path.join(config.dame_path, "bakamitai_template.mp3"))  # NOSONAR
    print("done")

# make damedane
import sys

sys.path.insert(1, config.first_order_model_path)  # 다메다메 프로젝트 레포지토리를 추가하여 import 가능하게 조치
import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.transform import resize
import warnings
from demo import load_checkpoints, make_animation  # noqa # NOSONAR
from skimage import img_as_ubyte


def convert_image_to_video(upload_image, output_path):
    print("다메다메 밈 작업중", end=' ')
    warnings.filterwarnings("ignore")

    source_image = imageio.imread(upload_image)
    driving_video = imageio.mimread(os.path.join(config.dame_path, '04.mp4'))

    source_image = resize(source_image, (256, 256))[..., :3]
    driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]

    generator, kp_detector = load_checkpoints(
        config_path=os.path.join(config.first_order_model_path, 'config/vox-256.yaml'),
        checkpoint_path=os.path.join(config.dame_path, 'vox-cpk.pth.tar'))

    # make video
    predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True)
    imageio.mimsave(output_path, [img_as_ubyte(frame) for frame in predictions])
    print('done')
    return output_path


def make_damedame(upload_image_path, output: str = os.path.join(config.video_path, 'result.mp4')):
    [filename, ext] = os.path.splitext(output)
    origin_path = filename + "-origin" + ext
    sub_path = filename + "-3x" + ext

    convert_image_to_video(upload_image_path,
                           origin_path)

    # 3배 빠르기로 비디오 변경, 오디오 소스 추가
    print("영상 오디오 소스 추가 및 배속 변경 중", end=' ')
    video.convert3x_faster_video(origin_path, sub_path)
    video.insert_audio_on_video(sub_path,
                                os.path.join(config.dame_path, "bakamitai_template.mp3"),  # NOSONAR
                                output)

    if os.path.exists(origin_path):
        os.remove(origin_path)

    if os.path.exists(sub_path):
        os.remove(sub_path)
    print('done')
    return output


# print(__file__, "모듈 리소스 로드 완료")

if __name__ == "__main__":
    print("다메다메 모듈을 테스트 진행합니다.")
    print("테스트 이미지 다운로드")
    urllib.request.urlretrieve(
        "https://lab.ssafy.com/s04-ai-image-sub2/s04p22d101/uploads/95c86ac00bb9068fbaddfde923ea99f8/goo.jpg",
        r"C:\content\damesource\image.png")
    path = make_damedame(r"C:\content\damesource\image.png")
    print("최종 결과물", path)
