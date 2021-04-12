import os

import uuid
import re
import json

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

import urllib.request
import httpx


from init import init

init()

from utils import db, url, video
from config import config

from PIL import Image

if not config.IS_AWS_SERVER:
    from src import damedame as dame
    from src import startfaceswap as faceswap
    from src import MODNetVideo

app = FastAPI()

# 여기부터 메인기능 시작 ###


#  S04P22D101-54	백엔드 RESTful API 프로토콜 / 가짜 격언 생성 기능에서 얼굴 합성 딥페이크
# input : origin위인 사진, target합성할 얼굴 사진
# output : 합성된 사진 (위인 사진 기준)
@app.post("/api/v1/deepfake", name="얼굴 합성 딥페이크 서비스")
async def create_deep_fake_image(origin: UploadFile = File(...), target: UploadFile = File(...)):  # NOSONAR
    content_origin = await origin.read()
    ext = origin.filename[origin.filename.rfind('.'):]
    origin.filename = str(uuid.uuid4()).replace('-', '') + ext

    content_target = await target.read()
    ext = target.filename[target.filename.rfind('.'):]
    target.filename = str(uuid.uuid4()).replace('-', '') + ext

    origin_input = os.path.join(config.face_swap_img_path, origin.filename)
    target_input = os.path.join(config.face_swap_img_path, target.filename)
    output = os.path.join(config.face_swap_result_path, str(uuid.uuid4()).replace('-', '') + ".png")

    print("origin_input:", origin_input)
    print("target_input:", target_input)

    with open(origin_input, "wb") as fp:
        fp.write(content_origin)
    with open(target_input, "wb") as fp:
        fp.write(content_target)

    # AWS 서버는 자체적으로 GPU 연산을 할 수 없기에 위임하여 이를 처리
    if config.IS_AWS_SERVER:
        async with httpx.AsyncClient() as client:
            files = {'origin': (origin.filename, content_origin, "application/octet-stream"),  # NOSONAR
                     'target': (target.filename, content_target, "application/octet-stream")}  # NOSONAR
            r = await client.post(config.GPU_SERVER_DOMAIN + "/api/v1/deepfake", files=files,
                                  timeout=httpx.Timeout(300.0, connect=5.0))
            if r.status_code != httpx.codes.OK:
                return JSONResponse(status_code=r.status_code, content={
                    "message": "서버 내에서 위임 작업 중에 문제가 발생하였습니다. " + r.raise_for_status()})  # NOSONAR
            data = json.loads(r.text)
            urllib.request.urlretrieve(
                config.GPU_SERVER_DOMAIN + data["url"],
                filename=output)
    else:
        faceswap.makedeepface(upload_origin_image_path=origin_input, upload_target_image_path=target_input,
                                output=output)
    return {"url": url.convert_path_to_url(output, base_url="/api/v1/content/")}  # NOSONAR


#  S04P22D101-55	백엔드 RESTful API 프로토콜 / 다메다메 짤 생성
# input : 합성할 얼굴 사진
# output : 합성된 동영상
@app.post("/api/v1/damedame", name="다메다메 짤 생성 서비스")
async def create_dame_meme_video(image: UploadFile = File(...)):  # NOSONAR
    contents = await image.read()
    image.filename = image.filename.replace(' ', '')
    input_path = os.path.join(config.image_path, image.filename)
    output_path = os.path.join(config.video_path, str(uuid.uuid4()).replace('-', '') + ".mp4")
    with open(input_path, "wb") as fp:
        fp.write(contents)
    print("input:", input_path)
    # AWS 서버는 자체적으로 GPU 연산을 할 수 없기에 위임하여 이를 처리
    if config.IS_AWS_SERVER:
        async with httpx.AsyncClient() as client:
            files = {'image': (image.filename, contents, "application/octet-stream")}  # NOSONAR
            r = await client.post(config.GPU_SERVER_DOMAIN + "/api/v1/damedame", files=files,
                                  timeout=httpx.Timeout(300.0, connect=5.0))
            if r.status_code != httpx.codes.OK:
                return JSONResponse(status_code=r.status_code, content={
                    "message": "서버 내에서 위임 작업 중에 문제가 발생하였습니다. " + r.raise_for_status()})  # NOSONAR
            data = json.loads(r.text)
            urllib.request.urlretrieve(
                config.GPU_SERVER_DOMAIN + data["url"],
                filename=output_path)
    else:
        dame.make_damedame(upload_image_path=input_path, output=output_path)
    return {"url": url.convert_path_to_url(output_path, base_url="/api/v1/content/")}  # NOSONAR


#  S04P22D101-56	백엔드 RESTful API 프로토콜 / 동영상 배경 삭제 및 배경 변경
# input : 동영상, 배경사진
# output : 합성된 동영상
@app.post("/api/v1/removeBg", name="동영상 배경 변경 서비스")
async def remove_back_ground_on_video(video: UploadFile = File(...), image: UploadFile = File(...)):  # NOSONAR
    print("배경바꾸기 시작합니다")
    image_contents = await image.read()
    ext = image.filename[image.filename.rfind('.'):]
    image.filename = str(uuid.uuid4()).replace('-', '') + ext
    input_image_path = os.path.join(config.image_path, image.filename)

    video_contents = await video.read()
    ext = video.filename[video.filename.rfind('.'):]
    video.filename = str(uuid.uuid4()).replace('-', '') + ext
    input_video_path = os.path.join(config.video_path, video.filename)

    output_path = os.path.join(config.video_path, str(uuid.uuid4()).replace('-', '') + ".mp4")

    with open(input_image_path, "wb") as fp:
        fp.write(image_contents)

    with open(input_video_path, "wb") as fp:
        fp.write(video_contents)

    print("input_image:", input_image_path)
    print("input_video:", input_video_path)
    # AWS 서버는 자체적으로 GPU 연산을 할 수 없기에 위임하여 이를 처리
    if config.IS_AWS_SERVER:
        async with httpx.AsyncClient() as client:
            files = {'video': (video.filename, video_contents, "application/octet-stream"),  # NOSONAR
                     'image': (image.filename, image_contents, "application/octet-stream")}  # NOSONAR
            r = await client.post(config.GPU_SERVER_DOMAIN + "/api/v1/removeBg", files=files,
                                  timeout=httpx.Timeout(300.0, connect=5.0))
            if r.status_code != httpx.codes.OK:
                return JSONResponse(status_code=r.status_code, content={
                    "message": "서버 내에서 위임 작업 중에 문제가 발생하였습니다. " + r.raise_for_status()})  # NOSONAR
            data = json.loads(r.text)
            urllib.request.urlretrieve(
                config.GPU_SERVER_DOMAIN + data["url"],
                filename=output_path)
    else:
        MODNetVideo.bg_remove(input_video_path, input_image_path, output_path)
    return {"url": url.convert_path_to_url(output_path, base_url="/api/v1/content/")}  # NOSONAR


@app.get("/api/v1/content/{rest_of_path:path}", name="파일 가져오기")
async def serve_upload_file(rest_of_path: str, download: bool = False):
    print("다운로드")
    file_path = os.path.join(config.root, rest_of_path)
    if os.path.exists(file_path):
        if download:
            return FileResponse(file_path, media_type="application/octet-stream")  # NOSONAR
        return FileResponse(file_path)
    else:
        return JSONResponse(status_code=400, content={"message": "존재하지 않는 파일입니다."})


# S04P22D101-106     최근 게시글 조회에 필요한 썸네일 생성
# input : 만들어진 output의 파일 경로, type(0 - 이미지, 1 - 동영상)
# output : 썸네일(이름은 board_no.jpg)
CONTENT_MATCH = re.compile("(?:content/)(.*(?:png|mp4))")


@app.get("/api/v1/thumbnails/{rest_of_path:path}", name="썸네일 호출 및 만들기")
async def serve_thumbnails(
        rest_of_path: str,
        # board_no: int,
        # type: int,
):
    print("Thumbnails 제작 및 호출")
    thumbnail_path: str = os.path.join(config.thumbnail_path, rest_of_path)
    no_image_path: str = os.path.join(config.image_path, "no_image.png")

    # 이미 해당 썸네일이 존재하는 경우. 해당 썸네일 반환
    if os.path.exists(thumbnail_path):
        return FileResponse(thumbnail_path)

    path, ext = os.path.splitext(thumbnail_path)
    board_no_str = os.path.basename(path)

    if board_no_str.isdigit() is False or ext != '.png':
        return JSONResponse(status_code=400, content={"message": "잘못된 파일이름 또는 잘못된 확장자를 호출하였습니다."})

    board_no = int(board_no_str)

    # DB select board by no
    board_info = await db.find_board_detail_by_board_no(int(board_no))
    if not board_info:
        return JSONResponse(status_code=400, content={"message": "존재하지 않는 게시글 입니다."})
    global CONTENT_MATCH
    data = CONTENT_MATCH.findall(board_info["content"])
    if not data:
        # no_image_준비
        image = Image.open(no_image_path)
        image_resize = image.resize((425, 265))
        image_resize.save(thumbnail_path)
        # return JSONResponse(status_code=400, content={"message": "해당 게시글에 썸네일을 만들 수 있는 리소스가 존재치 않습니다."})
        return FileResponse(thumbnail_path)

    print(board_info)
    # create thumbnails
    resource_path = os.path.join(config.root, data[0])
    if not os.path.exists(resource_path):
        # no_image_준비
        image = Image.open(no_image_path)
        image_resize = image.resize((425, 265))
        image_resize.save(thumbnail_path)
        # return JSONResponse(status_code=500, content={"message": "서버 내에서 게시글에 있는 리소스 파일을 찾을 수 없습니다."})
        return FileResponse(thumbnail_path)
    ext = os.path.splitext(resource_path)[-1]

    # Image
    if ext == '.png':
        try:
            # if os.path.isfile(image_path) is False:
            image = Image.open(resource_path)
            image_resize = image.resize((425, 265))
            image_resize.save(thumbnail_path)
            return FileResponse(thumbnail_path)
        except IOError:
            return JSONResponse(status_code=400, content={"message": "썸네일 제작중 에러가 발생했습니다."})
    elif ext == '.mp4':
        try:
            path, ext = os.path.splitext(thumbnail_path)
            print(ext)
            mid_image = path + "-mid" + ext
            # if os.path.isfile(output) is False:
            video.create_video_thumbnail(input_video_path=resource_path, output_image_path=mid_image)
            image = Image.open(mid_image)
            image_resize = image.resize((425, 265))
            image_resize.save(thumbnail_path)
            os.remove(mid_image)
            return FileResponse(thumbnail_path)
        except IOError:
            return JSONResponse(status_code=400, content={"message": "썸네일 제작중 에러가 발생했습니다."})
    else:
        return JSONResponse(status_code=400, content={"message": "게시글에 포함된 리소스가 썸네일을 생성할 수 없는 확장자를 가지고 있습니다."})


# 여기까지 메인기능 종료 ###


# 여기부터 게시글 기능 시작 ###

#  S04P22D101-63	백엔드 RESTful API 프로토콜 / 최근 게시글들 조회(추천순 반영)
@app.get("/api/v1/board/good", name="전체 게시글 조회(24시간 내, 좋아요 많은 순)")
async def find_all_board_on_day_by_good(
        page_count: int
):
    result = await db.find_all_board_on_day_by_good(page_count)
    if result is None:
        return JSONResponse(status_code=400, content={"message": "좋아요 기준 게시글 조회에 실패하였습니다."})
    return {"items": result}


#  S04P22D101-63	백엔드 RESTful API 프로토콜 / 최근 게시글들 조회(추천순 반영)
@app.get("/api/v1/board/view", name="전체 게시글 조회(24시간 내, 조회많은 순)")
async def find_all_board_on_day_by_view(
        page_count: int
):
    result = await db.find_all_board_on_day_by_view(page_count)
    if result is None:
        return JSONResponse(status_code=400, content={"message": "조회수 기준 게시글 조회에 실패하였습니다."})
    return {"items": result}


#  S04P23D101-71	백엔드 RESTful API 프로토콜 / 최근 게시글들 조회(추천순 반영)
@app.get("/api/v1/board/newest", name="전체 게시글 조회(24시간 내, 최신 순)")
async def find_all_board_on_day_by_board_no(
        page_count: int
):
    result = await db.find_all_board_on_day_by_newest(page_count)
    if result is None:
        return JSONResponse(status_code=400, content={"message": "조회수 기준 게시글 조회에 실패하였습니다."})
    return {"items": result}


#  S04P22D101-64     백엔드 RESTful API 프로토콜 / 게시글 상세 조회
@app.get("/api/v1/board/detail/{board_no}", name="게시글 상세 조회")
async def find_board_detail_by_board_no(board_no: int):
    await db.increase_view_count(board_no)
    result = await db.find_board_detail_by_board_no(board_no)
    if result is None:
        return JSONResponse(status_code=400, content={"message": "존재하지 않는 게시글입니다."})
    return result


#  S04P22D101-57	백엔드 RESTful API 프로토콜 / 게시글 작성(공유)
# input : content(게시글 내용), content_type(게시글 내용 - 구분용), nickname(익명 닉네임), password(비밀번호)
# output : 게시글 작성 성공 유무
class BoardWriteInfoRequest(BaseModel):
    title: str
    content: str
    content_type: str
    nickname: str
    password: str


@app.post("/api/v1/board/write", name="게시글 작성")
async def write_board(
        item: BoardWriteInfoRequest, request: Request
):
    ip = request.client.host
    board_info = {
        "title": item.title,
        "content": item.content,
        "content_type": item.content_type,
        "nickname": item.nickname,
        "password": item.password,
        "ip": ip
    }
    result = await db.write_board(board_info)
    if result is None:
        return JSONResponse(status_code=400, content={"message": "게시물 작성에 실패했습니다."})

    return result


#  S04P22D101-67     백엔드 RESTful API 프로토콜 / 게시글 수정
# output : 게시글 수정 성공 유무
class BoardEditInfoRequest(BaseModel):
    board_no: int
    title: str
    content: str
    content_type: str
    nickname: str
    password: str


@app.put("/api/v1/board/{board_no}", name="게시글 수정")
async def edit_board(
        board_no: int, item: BoardEditInfoRequest, request: Request
):
    print("게시판 수정")
    ip = request.client.host
    board_info = {
        "title": item.title,
        "content": item.content,
        "content_type": item.content_type,
        "nickname": item.nickname,
        "password": item.password,
        "ip": ip,
        "board_no": board_no
    }
    res_check = await db.check_password_on_board(item.password, board_no)

    if res_check:
        result = await db.edit_board(board_info)
        if result is None:
            return JSONResponse(status_code=400, content={"message": "게시물 수정에 실패했습니다."})
        return result
    else:
        return JSONResponse(status_code=400, content={"message": "비밀번호가 일치하지 않습니다."})  # NOSONAR


#  S04P22D101-60	백엔드 RESTful API 프로토콜 / 게시글 삭제
# input : board_no(보드번호), password(비밀번호)
# output :  게시글 삭제 성공 유무
class PasswordRequest(BaseModel):
    password: str


@app.delete("/api/v1/board/{board_no}", name="게시글 삭제")
async def delete_board(
        board_no: int,
        password: str,
):
    res_check = await db.check_password_on_board(password, board_no)
    if res_check:
        result = await db.delete_board(board_no)

        if result is None:
            return JSONResponse(status_code=400, content={"message": "게시물 삭제에 실패했습니다."})
        return result
    else:
        return JSONResponse(status_code=400, content={"message": "비밀번호가 일치하지 않습니다."})  # NOSONAR


#  S04P22D101-62	백엔드 RESTful API 프로토콜 / 게시글 추천(좋아요 기능)
# input : board_no(보드번호)
# output : 좋아요 성공 유무 (중복 방지)
@app.post("/api/v1/board/like/{board_no}", name="게시글 추천(좋아요 기능)")
async def count_up_thumbs_up_on_board(
        board_no: int, request: Request
):
    ip = request.client.host
    await db.decrease_view_count(board_no)
    res_check = await check_user_ip_on_good_list(board_no, ip)

    if res_check['result'] is None:
        return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})  # NOSONAR

    # 존재했으면 이미 누른 상태이므로 -1
    if res_check['result']:
        count_result = await db.count_down_thumbs_up_on_board(board_no)
        if count_result is None:
            return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})  # NOSONAR

        delete_result = await db.delete_user_ip_on_good_list(board_no, ip)
        if delete_result is None:
            await db.count_up_thumbs_up_on_board(board_no)
            return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})  # NOSONAR
        return "좋아요 취소"

    # 존재하지 않았음 좋아요+1
    else:
        count_result = await db.count_up_thumbs_up_on_board(board_no)
        if count_result is None:
            return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})  # NOSONAR
        insert_result = await db.insert_user_ip_on_good_list(board_no, ip)

        if insert_result is None:
            await db.count_down_thumbs_up_on_board(board_no)
            return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})  # NOSONAR
        return "좋아요!"


# S04P22D101-105    추천 중복 방지
# input : board_no(보드번호), ip(유저ip)
# output : 좋아요 성공 유무 (중복 방지)
async def check_user_ip_on_good_list(
        board_no: int,
        ip: str,
):
    result = await db.check_user_ip_on_good_list(board_no, ip)
    return {"result": result}


class ShareBoardWriteInfoRequest(BaseModel):
    content: str
    content_type: str


@app.post("/api/v1/share/kakao", name="게시글 카카오 공유")
async def share_board(
        item: ShareBoardWriteInfoRequest, request: Request
):
    ip = request.client.host
    print(item)
    board_info = {
        "content": item.content,
        "content_type": item.content_type,
        "nickname": "익명",
        "ip": ip
    }
    result = await db.write_share_board(board_info)
    if result is None:
        return JSONResponse(status_code=400, content={"message": "게시물 작성에 실패했습니다."})

    result["url"] = "/api/v1/share/kakao/" + result["s_board_no"]
    return result


@app.get("/api/v1/share/kakao/{s_board_no}", name="공유 게시글 번호로 조회")
async def find_share_board(
        s_board_no: int
):
    result = await db.find_share_board_detail_by_board_no(s_board_no)
    if result is None:
        return JSONResponse(status_code=400, content={"message": "게시물 조회에 실패했습니다."})

    return result


# 여기까지 게시글 기능 종료 ###


# 여기부터 댓글 기능 시작 ###

#  S04P22D101-65     백엔드 RESTful API 프로토콜 / 댓글 조회 (해당 게시글에 대해)
@app.get("/api/v1/comment/{board_no}", name="댓글 조회")
async def find_comment_by_board_no(
        board_no: int
):
    result = await db.find_comment_by_board_no(board_no)

    if result is None:
        return JSONResponse(status_code=400, content={"message": "댓글 조회에 실패했습니다."})
    return result


#  S04P22D101-59	백엔드 RESTful API 프로토콜 / 댓글 작성
# input : board_no(보드번호), content(댓글 내용), nickname(닉네임), password(비밀번호)
# output : 댓글 작성 성공 유무
class CommentWriteInfoRequest(BaseModel):
    content: str
    nickname: str
    password: str


@app.post("/api/v1/comment/write/{board_no}", name="댓글 작성")
async def write_comment(
        board_no: int, item: CommentWriteInfoRequest, request: Request
):
    ip = request.client.host
    comment_info = {
        "board_no": board_no,
        "content": item.content,
        "nickname": item.nickname,
        "password": item.password,
        "ip": ip,
    }

    result = await db.write_comment(comment_info)

    if result is None:
        return JSONResponse(status_code=400, content={"message": "댓글 작성에 실패했습니다."})
    return result


#  S04P22D101-61	백엔드 RESTful API 프로토콜 / 댓글 삭제
# input : comment_no(댓글번호), password(비밀번호)
# output : 댓글 삭제 성공 유무

@app.delete("/api/v1/comment/{comment_no}", name="댓글 삭제")
async def delete_comment(
        comment_no: int,
        password: str
):
    res_check = await db.check_password_on_comment(password, comment_no)
    if res_check:
        result = await db.delete_comment(comment_no)

        if result is None:
            return JSONResponse(status_code=400, content={"message": "댓글 삭제에 실패했습니다."})
        return result
    else:
        return JSONResponse(status_code=400, content={"message": "비밀번호가 일치하지 않습니다."})  # NOSONAR


#  S04P22D101-66     백엔드 RESTful API 프로토콜 / 댓글 수정
# output : 댓글 수정 성공 유무
@app.put("/api/v1/comment/{comment_no}", name="댓글 수정")
async def edit_comment(
        comment_no: int, content: str, nickname: str, password: str, request: Request
):
    ip = request.client.host
    comment_info = {
        "comment_no": comment_no,
        "content": content,
        "nickname": nickname,
        "password": password,
        "ip": ip
    }

    res_check = await db.check_password_on_comment(password, comment_no)
    if res_check:
        result = await db.edit_comment(comment_info)

        if result is None:
            return JSONResponse(status_code=400, content={"message": "댓글 수정에 실패했습니다."})
        return result
    else:
        return JSONResponse(status_code=400, content={"message": "비밀번호가 일치하지 않습니다."})  # NOSONAR


#  S04P22D101-85     백엔드 RESTful API 프로토콜 / 게시글 비밀번호 체크
# input : comment_no(댓글번호), password(비밀번호)
# output : 비밀번호 매칭 유무
@app.post("/api/v1/board/check/{board_no}", name="게시글 비밀번호 체크")
async def check_board(
        board_no: int, item: PasswordRequest
):
    result = await db.check_password_on_board(item.password, board_no)
    return {"result": result}


#  S04P22D101-86     백엔드 RESTful API 프로토콜 / 댓글 비밀번호 체크
# input : comment_no(댓글번호), password(비밀번호)
# output : 비밀번호 매칭 유무
@app.post("/api/v1/comment/check/{comment_no}", name="댓글 비밀번호 체크")
async def check_comment(
        comment_no: int, item: PasswordRequest
):
    result = await db.check_password_on_comment(item.password, comment_no)
    return {"result": result}


# 여기까지 댓글 기능 종료 ###

# 업로드 기능
@app.post("/api/v1/upload")
async def create_upload_files(file: UploadFile = File(...)):
    contents = await file.read()
    ext: str = os.path.splitext(file.filename)[-1]
    ext = ext if ext.startswith('.') else ''
    filename = str(uuid.uuid4()).replace('-', '') + ext
    path = os.path.join(config.upload_path, filename)
    with open(path, "wb") as fp:
        fp.write(contents)
    return {"url": url.convert_path_to_url(path, base_url="/api/v1/content/")}  # NOSONAR


# 데모 코드
@app.get("/")
async def read_root():
    return {"Hello": "World"}

