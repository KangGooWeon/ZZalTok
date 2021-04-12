<template>
  <div>
    <br /><br />
    <v-row justify="center">
      <v-dialog v-model="dialog" persistent max-width="600px">
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            class="ma-4"
            dark
            v-bind="attrs"
            v-on="on"
            large
            fab
            color="indigo"
            @click="changeZIndex()"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn class="ma-4" large fab color="primary" @click="aClick">
            <a
              style="color: white"
              id="downloadPhoto"
              download="my-photo.jpg"
              class="button"
              role="button"
              @click="down"
              ><i class="fas fa-download fa-2x"></i> <!-- Compliant icon fonts usage -->
            </a>
          </v-btn>
        </template>
        <v-card>
          <v-card-title class="headline">
            <div class="board_share_title">게시판 작성</div>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row no-gutters>
                <v-col cols="6">
                  <v-text-field
                    outlined
                    label="닉네임*"
                    required
                    v-model="boardWriteInfo.nickname"
                  ></v-text-field>
                </v-col>
                <v-spacer></v-spacer>
                <v-col cols="5">
                  <v-text-field
                    outlined
                    label="비밀번호*"
                    type="password"
                    required
                    v-model="boardWriteInfo.password"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    outlined
                    label="제목*"
                    required
                    v-model="boardWriteInfo.title"
                  ></v-text-field>
                </v-col>
                <v-textarea
                  outlined
                  placeholder="내용입력"
                  v-model="boardWriteInfo.content"
                ></v-textarea>
              </v-row>
              <small style="color: red" class="ml-2">*필수입력항목</small>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <div class="mb-3 mr-2">
              <v-btn color="blue darken-1" text @click="boardWrite"
                >글쓰기</v-btn
              >
              <v-btn color="blue darken-1" text @click="dialog = false"
                >취소</v-btn
              >
            </div>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
    <br />
  </div>
</template>

<script>
import http from "@/util/http-common.js";

export default {
  data() {
    return {
      dialog: false,

      kakaoShareInfo: {
        content: "",
        content_type: "",
      },
      boardWriteInfo: {
        title: "",
        content: "",
        content_type: "",
        nickname: "",
        password: "",
      },
    };
  },

  props: {
    downloadLink: { Type: String },
    contentType: { Type: String },
  },
  methods: {
    changeZIndex() {
      document.getElementsByClassName("__cov-contrl-content")[0].style.zIndex = 1;
    },
    aClick() {
      document.getElementById("downloadPhoto").click();
    },
    kakaoShare() {
      // console.log("카카오 공유하기");
      this.kakaoShareInfo.content = `{"url":"${this.downloadLink}"}`;
      this.kakaoShareInfo.content_type = this.contentType;
      // console.log(this.kakaoShareInfo);

      http
        .post("/v1/share/kakao", this.kakaoShareInfo)
        .then((response) => {
          // console.log(response);
          // console.log(response.data.s_board_no);
          //카카오 페이지
        })
        .catch((error) => {
          // console.log("에러 + 에러내용");
          console.log(error);
          // console.log(error.response);
        });
    },
    down() {
      const download = document.getElementById("downloadPhoto");

      if (this.contentType == "image") {
        //이미지 일때
        download.setAttribute("download", "my-photo.jpg");
      } else if (this.contentType == "video") {
        //비디오 일 때
        download.setAttribute("download", "my-video.mp4");
      }

      // console.log(download);
      download.setAttribute("href", this.downloadLink); //파일생성
    },
    boardWrite() {
      this.dialog = false; // dialog 창끄기

      this.boardWriteInfo.content = `{"url":"${this.downloadLink}", "content":"${this.boardWriteInfo.content}"}`;
      // this.boardWriteInfo.content = JSON.parse(this.boardWriteInfo.content); //content 안에 url, content 넣어주기

      this.boardWriteInfo.content_type = this.contentType; //컨텐트 타입넣어주기

      // console.log(this.boardWriteInfo);
      // test , sdf
      http
        .post("/v1/board/write", this.boardWriteInfo)
        .then((res) => {
          this.$store
            .dispatch("mainStore/findShareDetail", res.data.board_no)
            .then(() => {
              // console.log("이동합니다");
              this.$router.push(`/shareDetail?no=${res.data.board_no}`);
            })
            .catch((error) => {
              // console.log("에러", error);
              // console.log("에러내용", error.response);
            });
        })
        .catch((error) => {
          // console.log("에러 + 에러내용");
          console.log(error);
          // console.log(error.response);
        });
    },
  },
};
</script>

<style>
.board_share_title {
  width: 100%;
  text-align: center;
}
</style>
