<template>
  <div>
    <comment-form :type="'create'" :no="getShareDetail.board_no" />

    <v-divider></v-divider>

    <v-row class="mt-1">
      <v-col cols="1" md="1"></v-col>
      <v-col cols="12" md="10">
        <comment-list-item
          v-for="item in getCommentItems"
          :key="item.comment_no"
          :comment_no="item.comment_no"
          :content="item.content"
          :ip="item.ip"
          :nickname="item.nickname"
          :regdate="timeForToday(item.regdate)"
        />
      </v-col>
      <v-col cols="1" md="1"></v-col>
    </v-row>
  </div>
</template>

<script>
import CommentForm from "./CommentForm.vue";
import CommentListItem from "./CommentListItem.vue";
import { mapGetters } from "vuex";

export default {
  components: { CommentListItem, CommentForm },
  computed: {
    ...mapGetters("mainStore", ["getCommentItems", "getShareDetail"]),
  },
  methods:{
     timeForToday(value) {
      const today = new Date();
      const timeValue = new Date(value);

      const betweenTime = Math.floor(
        (today.getTime() - timeValue.getTime()) / 1000 / 60
      );
      if (betweenTime < 1) return "방금전";
      if (betweenTime < 60) {
        return `${betweenTime}분전`;
      }

      const betweenTimeHour = Math.floor(betweenTime / 60);
      if (betweenTimeHour < 24) {
        return `${betweenTimeHour}시간전`;
      }

      const betweenTimeDay = Math.floor(betweenTime / 60 / 24);
      if (betweenTimeDay < 365) {
        return `${betweenTimeDay}일전`;
      }
    },
  }
};
</script>