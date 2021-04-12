import os
from config import config
from distutils.dir_util import copy_tree


def init():
    # root 폴더 생성
    if not os.path.isdir(config.root):
        os.makedirs(config.root, exist_ok=True)
    # video 폴더 생성
    if not os.path.isdir(config.video_path):
        os.makedirs(config.video_path, exist_ok=True)

    # images 폴더 생성
    if not os.path.isdir(config.image_path):
        os.makedirs(config.image_path, exist_ok=True)
    
    # 딥페이크 폴더 생성
    if not os.path.isdir(config.face_swap_img_path):
        os.makedirs(config.face_swap_img_path, exist_ok=True)

    # thumbnails 폴더 생성
    if not os.path.isdir(config.thumbnail_path):
        os.makedirs(config.thumbnail_path, exist_ok=True)

    # content 필요한 리소스들을 이동
    copy_tree('./content', config.root)