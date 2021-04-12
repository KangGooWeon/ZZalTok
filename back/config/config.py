import os
import platform

# GPU 서버여부 체크
IS_GPU_SERVER: bool = 'gpu' in platform.node() and platform.system() == "Linux"
IS_AWS_SERVER: bool = 'Yes' == os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False) and platform.system() == "Linux"

# 작업할 볼륨 또는 폴더 선정
root: str = os.path.join(os.path.splitdrive(os.getcwd())[0], "/content/") \
    if not IS_GPU_SERVER else os.path.join(os.path.expanduser("~"), 'content/')
image_path: str = os.path.join(root, "images/")
upload_path: str = os.path.join(root, "uploads/")
thumbnail_path: str = os.path.join(root, "thumbnails/")
dame_path: str = os.path.join(root, "damesource/")
first_order_model_path: str = os.path.join(root, "first-order-model/")
MODNet_model_path: str = os.path.join(root, "MODNet/")
modenet_src_path: str = os.path.join(root, "modnetsource/")
video_path: str = os.path.join(root, "video/")
ffmpeg_path: str = os.path.join(root, "ffmpeg/")
face_swap_model_path: str = os.path.join(root, "faceswap/")
face_swap_img_path: str = os.path.join(root, "swapimgs/")
face_swap_result_path: str = os.path.join(root, "faceswap_result/")

# 일부 전역 변수 저장
GPU_SERVER_DOMAIN: str = "http://ssafy4th.ddns.net:8000"  # NOSONAR
