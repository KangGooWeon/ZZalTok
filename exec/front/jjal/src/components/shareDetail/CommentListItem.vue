<template>
  <div>
    <div
      class="mt-5 mb-5 pt-3 pl-2"
      @mouseover="isMenu = true"
      @mouseleave="isMenu = false"
      @click="isMenu = !isMenu"
    >
      <v-avatar color="indigo" size="53" style="float: left" class="mr-3">
        <img :src="avatarUrl" alt="프로필">
      </v-avatar>
      <div style="padding-top: -10px">
        <div class="font-weight-bold subtitle-1">
          <span>{{ nickname }} </span>
          <span style="color: #a9a9a9; font-size: 13px">({{ ip }})</span>
          &middot;
          <span style="color: #a9a9a9; font-size: 13px">{{
            regdate
          }}{{avatarUrle}}</span>

          <div style="float: right" v-if="isMenu">
            <!-- 수정 -->
            <v-btn
              icon
              x-small
              color="primary"
              fab
              dark
              @click="pwdDialog('update')"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>

            <!-- 삭제 -->
            <v-btn
              icon
              x-small
              color="error"
              fab
              dark
              @click="pwdDialog('delete')"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </div>
        </div>
        <div class="subtitle-2">
          <span>{{ content }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CommentForm from "./CommentForm.vue";
import http from "@/util/http-common.js";
import { mapActions } from "vuex";
import Swal from "sweetalert2";

export default {
  props: {
    comment_no: { Type: Number },
    content: { Type: String },
    ip: { Type: String },
    nickname: { Type: String },
    regdate: { Type: String },
  },
  components: { CommentForm },
  data() {
    return {
      menu1: false,
      menu2: false,

      isMenu: false,
      isPwdDialog: false,

      //dialog부분
      dialogTitle: "",
      dialogContent: "",

      pwd: "",
      avatarUrl: "",
    };
  },

  methods: {
    ...mapActions("mainStore", ["deleteComment", "updateComment"]),
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
          this.findCommentPwd(str);
        }
      });
    },

    findCommentPwd(str) {
      let flag = false;
      http
        .post(`/v1/comment/check/${this.comment_no}`, { password: this.pwd })
        .then((res) => {
          // console.log("댓글 비빌번호 성공 : " + res.data.result);

          if (!res.data.result) {
            Swal.fire({
              icon: "error",
              title: "비밀번호가 틀립니다.",
            });
            return;
          }

          // 댓글 등록 수정
          if (str == "update") {
            Swal.fire({
              input: "textarea",
              inputLabel: "Message",
              inputPlaceholder: "댓글 내용을 등록해주세요",
              inputValue: this.content,
              showCancelButton: true,
            }).then((result) => {
              // console.log(result);
              if (result.isConfirmed) {
                let data = {};
                data.no = this.comment_no;
                data.content = result.value;
                data.nickname = this.nickname;
                data.password = this.pwd;
                this.updateComment(data);
              }
            });
          } else {
            this.deleteComment({ no: this.comment_no, password: this.pwd });
          }
        })
        .catch((error) => {
          console.log("에러", error);
          // console.log("에러내용", error.response);
        });

      return flag;
    },
  },
  created(){
    this.avatarUrl = require('../../assets/among'+(Math.floor(Math.random() * 10)+1)+'.png') // NOSONAR
  }
};
</script>

<style>
.comment-content {
  width: 90%;
}

.menu-input {
  border: 1px solid black;
  background-color: rgb(3, 3, 90);
  border-radius: 5px;
}

.menu-input input {
  background-color: white;
  border-radius: 5px;
  margin-left: 5px;
  padding-left: 5px;
  width: 150px;
}

.update-form {
  border: 1px solid black;
  border-radius: 5px;
}
</style>
