#! /usr/bin/env python
import os
import cv2
import git
from config import config

if not os.path.isdir(config.face_swap_model_path):
    print("딥페이크 프로젝트 클론 중")
    git.Repo.clone_from("https://github.com/getCurrentThread/FaceSwap", config.face_swap_model_path)

import sys

sys.path.insert(1, config.face_swap_model_path)  # 딥페이크 프로젝트 레포지토리를 추가하여 import 가능하게 조치

from face_detection import select_face  # noqa # NOSONAR
from face_swap import face_swap  # noqa # NOSONAR


class Arguments:
    src: str
    dst: str
    out: str
    warp_2d: bool
    correct_color: bool
    no_debug_window: bool

    def __init__(self, src, dst, out, warp_2d=True, correct_color=True, no_debug_window=True):
        self.src = src
        self.dst = dst
        self.out = out
        self.warp_2d = warp_2d
        self.correct_color = correct_color
        self.no_debug_window = no_debug_window


def make_deep_face(args):
    # Read images
    src_img = cv2.imread(args.src)
    dst_img = cv2.imread(args.dst)

    # Select src face
    src_points, src_shape, src_face = select_face(src_img)
    # Select dst face
    dst_points, dst_shape, dst_face = select_face(dst_img)

    if src_points is None or dst_points is None:
        print('Detect 0 Face !!!')
        # exit(-1)

    output = face_swap(src_face, dst_face, src_points, dst_points, dst_shape, dst_img, args)

    dir_path = os.path.dirname(args.out)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    cv2.imwrite(args.out, output)

    # For debug
    if not args.no_debug_window:
        cv2.imshow("From", dst_img)
        cv2.imshow("To", output)
        cv2.waitKey(0)

        cv2.destroyAllWindows()


def makedeepface(upload_origin_image_path, upload_target_image_path,
                 output: str = os.path.join(config.face_swap_result_path, 'result.png')):
    print("딥페이크 진행합니다.")
    make_deep_face(Arguments(upload_origin_image_path, upload_target_image_path, output))

    if os.path.exists(upload_origin_image_path):
        os.remove(upload_origin_image_path)

    if os.path.exists(upload_target_image_path):
        os.remove(upload_target_image_path)

    return output


if __name__ == "__main__":
    print("딥페이크 모듈 테스트 진행합니다.")
    root = config.face_swap_model_path
    src = os.path.join(root, "imgs/test6.jpg")
    dst = os.path.join(root, "imgs/test7.jpg")
    out = os.path.join(root, "results/output6_7.jpg")
    make_deep_face(Arguments(src, dst, out))
