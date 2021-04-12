import os
import sys

import cv2
import argparse
import numpy as np
from PIL import Image
from tqdm import tqdm

import torch
import torch.nn as nn
import torchvision.transforms as transforms

from config import config
import urllib.request
import git

from utils import video

if not os.path.isdir(config.MODNet_model_path):
    print("MODNet 프로젝트 클론 중")
    git.Repo.clone_from("https://github.com/ZHKKKe/MODNet", config.MODNet_model_path)

PRETRAINED_CKPT_FILEPATH = os.path.join(config.MODNet_model_path, 'pretrained/modnet_webcam_portrait_matting.ckpt')


if not os.path.isdir(os.path.dirname(PRETRAINED_CKPT_FILEPATH)):
    os.makedirs(os.path.dirname(PRETRAINED_CKPT_FILEPATH), exist_ok=True)

# pretrained 모델 다운로드
if not os.path.exists(PRETRAINED_CKPT_FILEPATH):
    urllib.request.urlretrieve("https://docs.google.com/uc?export=download&id=1Nf1ZxeJZJL8Qx9KadcYYyEmmlKhTADxX",
                               filename=PRETRAINED_CKPT_FILEPATH)

# MODNet 프로젝트 레포지토리를 추가하여 import 가능하게 조치
sys.path.insert(1, os.path.join(config.MODNet_model_path, "src/models"))

# 상대경로에 따른 모듈 import가 불가한 문제가 있어 해당 라인을 수정
if not os.path.exists(os.path.join(config.MODNet_model_path, 'modded.txt')):
    with open(os.path.join(config.MODNet_model_path, 'src/models/modnet.py'), 'r') as fp:
        data = fp.readlines()
    data[4] = "from backbones import SUPPORTED_BACKBONES\n"
    with open(os.path.join(config.MODNet_model_path, 'src/models/modnet.py'), 'w') as fp:
        fp.writelines(data)
    with open(os.path.join(config.MODNet_model_path, 'modded.txt'), "w") as fp:
        fp.write('src\models\modnet.py is modded')

from modnet import MODNet # noqa


torch_transforms = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ]
)


def matting(modnet, video, background, result, fps=30):
    # video capture
    vc = cv2.VideoCapture(video)

    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    if not rval:
        print('Failed to read the video: {0}'.format(video))
        exit()

    num_frame = vc.get(cv2.CAP_PROP_FRAME_COUNT)
    h, w = frame.shape[:2]
    if w >= h:
        rh = 512
        rw = int(w / h * 512)
    else:
        rw = 512
        rh = int(h / w * 512)
    rh = rh - rh % 32
    rw = rw - rw % 32

    # load background image
    def file_load(filename):
        im = cv2.imread(filename)
        if len(im.shape) == 2:
            im = im[:, :, None]
        if im.shape[2] == 1:
            im = np.repeat(im, 3, axis=2)
        elif im.shape[2] == 4:
            im = im[:, :, 0:3]
        return im

    back_image = file_load(background)

    # video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(result, fourcc, fps, (w, h))
    GPU = True if torch.cuda.device_count() > 0 else False

    print('Start matting...')
    with tqdm(range(int(num_frame)))as t:
        for c in t:  # NOSONAR
            frame_np = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_np = cv2.resize(frame_np, (rw, rh), cv2.INTER_AREA)

            frame_pil = Image.fromarray(frame_np)
            frame_tensor = torch_transforms(frame_pil)
            frame_tensor = frame_tensor[None, :, :, :]
            if GPU:
                frame_tensor = frame_tensor.cuda()

            with torch.no_grad():
                _, _, matte_tensor = modnet(frame_tensor, True)

            matte_tensor = matte_tensor.repeat(1, 3, 1, 1)
            matte_np = matte_tensor[0].data.cpu().numpy().transpose(1, 2, 0)
            height, width, _ = matte_np.shape

            back_image_np = cv2.resize(back_image, (width, height), cv2.INTER_AREA)
            back_image_np = cv2.cvtColor(back_image_np.astype(np.uint8), cv2.COLOR_RGB2BGR)
            view_np = matte_np * frame_np + (1 - matte_np) * back_image_np
            view_np = cv2.cvtColor(view_np.astype(np.uint8), cv2.COLOR_RGB2BGR)
            view_np = cv2.resize(view_np, (w, h))
            video_writer.write(view_np)

            rval, frame = vc.read()
            c += 1  # NOSONAR

    video_writer.release()
    print('Save the result video to {0}'.format(result))


def bg_remove(video_path: str, background_image_path: str, result_path: str, fps: int = 30):
    print('Load pre-trained MODNet...')
    pretrained_ckpt = PRETRAINED_CKPT_FILEPATH
    modnet = MODNet(backbone_pretrained=False)
    modnet = nn.DataParallel(modnet)

    GPU = True if torch.cuda.device_count() > 0 else False
    if GPU:
        print('Use GPU...')
        modnet = modnet.cuda()
        modnet.load_state_dict(torch.load(pretrained_ckpt))
    else:
        print('Use CPU...')
        modnet.load_state_dict(torch.load(pretrained_ckpt, map_location=torch.device('cpu')))
    modnet.eval()
    mid_path = os.path.splitext(result_path)
    mid_path = mid_path[0] + '-mid' + mid_path[1]
    matting(modnet, video_path, background_image_path, mid_path, fps)
    video.insert_audio_on_video_fps30(mid_path, video_path, result_path)
    return result_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # NOSONAR
    parser.add_argument('--video', type=str, default=r"C:\Users\YSM\Desktop\test\dance.mp4", help='input video file')
    parser.add_argument('--background-path', type=str, default=r"C:\Users\YSM\Desktop\test\green.jpg",
                        help="input image file")
    parser.add_argument('--result-type', type=str, default='fg', choices=['fg', 'matte'],
                        help='matte - save the alpha matte; fg - save the foreground')
    parser.add_argument('--fps', type=int, default=30, help='fps of the result video')

    print('Get CMD Arguments...')
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print('Cannot find the input video: {0}'.format(args.video))
        exit()

    print('Load pre-trained MODNet...')
    pretrained_ckpt = PRETRAINED_CKPT_FILEPATH
    modnet = MODNet(backbone_pretrained=False)
    modnet = nn.DataParallel(modnet)

    GPU = True if torch.cuda.device_count() > 0 else False
    if GPU:
        print('Use GPU...')
        modnet = modnet.cuda()
        modnet.load_state_dict(torch.load(pretrained_ckpt))
    else:
        print('Use CPU...')
        modnet.load_state_dict(torch.load(pretrained_ckpt, map_location=torch.device('cpu')))
    modnet.eval()

    result = os.path.splitext(args.video)[0] + '_{0}.mp4'.format(args.result_type)
    alpha_matte = True if args.result_type == 'matte' else False
    matting(args.video, args.background_path, result, args.fps)
