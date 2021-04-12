<template>
  <div class="hidden-md-and-up" style="float: right">
    <v-menu bottom left>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon v-bind="attrs" v-on="on" class="mt-5 mr-1">
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item v-for="(item, i) in listItem" :key="i" @click="move(i)">
          <v-list-item-title class="menu-choice">{{
            item.title
          }}</v-list-item-title>
        </v-list-item>
      </v-list>
      <a
        style="color: white; display: neon;"
        id="downloadDot"
        download="my-photo.jpg"
        class="button"
        role="button"
        @click="down"
      >
      </a>
    </v-menu>
  </div>
</template>

<script>
import http from "@/util/http-common.js";
import { mapActions, mapGetters } from "vuex";
import Swal from "sweetalert2";

export default {
  props: {
    board_no: { Type: Number },
    title: { Type: String },
    content: { Type: String },
    url: { Type: String },
    content_type: { Type: String },
    nickname: { Type: String },
  },
  computed: {
    ...mapGetters("mainStore", ["getShareDetail"]),
  },
  data() {
    return {
      pwd: "",
      listItem: [
        { title: "수정" },
        { title: "삭제" },
        { title: "다운로드" },
        { title: "공유" },
      ],
      feedSettings: {
        objectType: "feed",
        content: {
          title: this.title,
          description: this.content,
          imageUrl:
            "https://j4d101.p.ssafy.io/api/v1/content/thumbnails/" +
            this.board_no +
            ".png",
          link: {
            mobileWebUrl: `https://j4d101.p.ssafy.io/shareDetail?no=${this.board_no}`,
            webUrl: `https://j4d101.p.ssafy.io/shareDetail?no=${this.board_no}`,
          },
        },
        buttons: [
          {
            title: "웹으로 이동",
            link: {
              webUrl: `https://j4d101.p.ssafy.io/shareDetail?no=${this.board_no}`,
              mobileWebUrl: `https://j4d101.p.ssafy.io/shareDetail?no=${this.board_no}`,
            },
          },
          {
            title: "앱으로 이동",
            link: {
              webUrl: `https://j4d101.p.ssafy.io/shareDetail?no=${this.board_no}`,
              mobileWebUrl: `https://j4d101.p.ssafy.io/shareDetail?no=${this.board_no}`,
            },
          },
        ],
      },
    };
  },

  methods: {
    ...mapActions("mainStore", ["updateShareDetail", "deleteShareDetail"]),
    move(number) {
      // console.log(number);
      switch (number) {
        case 0:
          this.pwdDialog("update");
          break;
        case 1:
          this.pwdDialog("delete");
          break;
        case 2:
          // console.log("ddd")
          document.getElementById("downloadDot").click();
          break;
        case 3:
          this.kakaoShare();
          break;
      }
    },
    pwdDialog(str) {
      Swal.fire({
        title: "비밀번호를 입력해주세요",
        input: "password",
        width: 500,
        inputAttributes: {
          autocapitalize: "off",
        },
        showCancelButton: true,
        confirmButtonText: "Ok",
        showLoaderOnConfirm: true,
        allowOutsideClick: () => !Swal.isLoading(),
      }).then((result) => {
        // console.log(result);
        if (result.isConfirmed) {
          this.pwd = result.value;
          this.findshareDetailPwd(str);
        }
      });
    },

    kakaoShare() {
      this.feedSettings.content.title = this.title;
      this.feedSettings.content.description = this.content;
      Kakao.Link.sendDefault(this.feedSettings);
    },

    findshareDetailPwd(str) {
      http
        .post(`/v1/board/check/${this.board_no}`, { password: this.pwd })
        .then((res) => {
          // console.log("게시판 비빌번호 성공 : " + res.data.result);

          if (!res.data.result) {
            Swal.fire({
              icon: "error",
              title: "비밀번호가 틀립니다.",
            });
            return;
          }

          // 게시판 수정
          if (str == "update") {
            Swal.fire({
              showCancelButton: true,
              html:
                `제목<input id="swal-input1" class="swal2-input" value="${this.title}">` +
                `내용<textarea id="swal-input2" class="swal2-input" style="height:150px">${this.content}</textarea>`,
              focusConfirm: false,
              preConfirm: () => {
                return [
                  document.getElementById("swal-input1").value,
                  document.getElementById("swal-input2").value,
                ];
              },
            }).then((result) => {
              // console.log(result);
              if (result.isConfirmed) {
                let data = {};
                let temp = this.url.substr(this.url.indexOf("/api"));
                // console.log(temp);
                data.board_no = this.board_no;
                data.title = result.value[0];
                data.content = `{"url":"${temp}", "content":"${result.value[1]}"}`;
                data.content_type = this.content_type;
                data.nickname = this.nickname;
                data.password = this.pwd;
                this.updateShareDetail(data);
              }
            });
          } else {
            this.deleteShareDetail({ no: this.board_no, password: this.pwd });
            this.$router.push({ name: "Main" });
          }
        })
        .catch((error) => {
          console.log("에러", error);
          console.log("에러내용", error.response);
        });
    },
    down() {
      const download = document.getElementById("downloadDot");

      if (this.content_type == "image") {
        //이미지 일때
        download.setAttribute("download", "my-photo.jpg");
      } else {
        //비디오 일 때
        download.setAttribute("download", "my-video.mp4");
      }

      // console.log("콘텐트타입" + this.content_type);
      download.setAttribute("href", this.url); //파일생성
    },
  },

  mounted() {
    Kakao.Link.createDefaultButton(
      Object.assign({}, this.feedSettings, { container: ".kakao-link" })
    );
    // console.log("여기확인:" + this.feedSettings.content.title);
    // console.log("여기확인:" + this.feedSettings.content.description);
  },
};
</script>