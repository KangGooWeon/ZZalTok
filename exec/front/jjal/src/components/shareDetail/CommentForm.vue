<template>
  <v-row class="mt-2 pt-4">
    <v-col cols="1" md="1"></v-col>
    <v-col cols="12" md="3">
      <v-text-field
        outlined
        label="NickName"
        height="10px"
        class=""
        ref="nickName"
        v-model="item.nickname"
      ></v-text-field>

      <v-text-field
        outlined
        type="password"
        label="PassWord"
        height="10px"
        password
        ref="password"
        v-model="item.password"
      ></v-text-field>
    </v-col>

    <v-col cols="12" md="7">
      <v-textarea
        outlined
        label="내용을 입력하세요"
        auto-grow
        height="141px"
        ref="content"
        v-model="item.content"
        style="color: red"
      ></v-textarea>

      <div class="mb-5" style="float: right">
        <v-btn @click="checkHandler()">등록</v-btn>
      </div>
    </v-col>
    <v-col cols="1" md="1"></v-col>
  </v-row>
</template>

<script>
import { mapActions } from "vuex";

export default {
  props: {
    type : {Type :String},
    no: { Type: Number },
  },
  data() {
    return {
      data: {},
      item:{
        content: '',
        nickname: '',
        password: '',
      }
    };
  },
  methods: {
    ...mapActions('mainStore',["createComment"]),
    checkHandler() {
      let err = true;
      let msg = '';

      !this.item.nickname &&
        ((msg = '작성자를 입력해주세요'), (err = false));
      err &&
        !this.item.password &&
        ((msg = '비밀번호를 입력해주세요'), (err = false));
      err &&
        !this.item.content &&
        ((msg = '내용을 입력해주세요'), (err = false));

      if (!err) alert(msg);
      else this.type == 'create' ? this.createHandler() : this.updateHandler();
    },

    createHandler() {
      this.data.item = this.item;
      this.data.no = this.no;
      this.createComment(this.data);

      //값 초기화
      this.item.content = '';
      this.item.nickname = '';
      this.item.password = '';
    },

    updateHandler() {},

    created() {
      //update일때 값 담아주기
    },
  },
};
</script>
