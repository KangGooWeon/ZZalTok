<template>
  <v-container fluid class="back-img">
    <v-row class="mt-2">
      <v-col cols="1" md="2"></v-col>
      <v-col cols="12" md="8">
        <div class="box-shadow">
          <!-- 메뉴 -->
          <dot-menu
            :board_no="getShareDetail.board_no"
            :title="getShareDetail.title"
            :content="getShareDetail.content"
            :url="getShareDetail.url"
            :content_type="getShareDetail.content_type"
            :nickname="getShareDetail.nickname"
          />

          <div class="pt-3 pl-2">
            <v-avatar size="53" style="float: left" class="mr-3 mt-1">
              <v-img :src="avatarUrl" alt="John" />
            </v-avatar>
            <div style="padding-top: -10px">
              <div class="font-weight-bold title">
                <span>{{ getShareDetail.title }}</span>
              </div>
              <div class="subtitle-2">
                <span>{{ getShareDetail.nickname }} </span>
                <span style="font-size: 12px; color: #888888">({{ getShareDetail.ip }})</span>
              </div>
            </div>
          </div>
          <div>
            <v-img v-if="getShareDetail.content_type == 'image'" :src="getShareDetail.url" class="detail-img mt-3"> </v-img>
            <my-video
              v-if="getShareDetail.content_type == 'video'"
              :sources="getVideo()"
              :options="getOption()"
              style="max-width: 660px; min-width: 350px display: block; margin: 0px auto"
              @click="play()"
            ></my-video>
          </div>

          <div class="text-main">
            <v-sheet min-height="100px">
              <v-sheet>
                <v-row>
                  <v-col cols="1"></v-col>
                  <v-col cols="10">
                    <div class="pt-5 pl-5">{{ getShareDetail.content }}</div>

                    <div class="text-center mt-10">
                      <v-btn color="indigo" fab large dark @click="updateDetailLike(getShareDetail.board_no)">
                        <i class="fas fa-thumbs-up fa-lg"></i> <!-- Compliant icon fonts usage -->
                      </v-btn>
                      <div class="mt-3">
                        <i class="fas fa-thumbs-up mr-1"></i> <!-- Compliant icon fonts usage -->
                        {{ getShareDetail.good }}
                        <i class="far fa-eye ml-1"></i> <!-- Compliant icon fonts usage -->
                        {{ getShareDetail.view_cnt }}
                        <i class="fas fa-comment"></i> <!-- Compliant icon fonts usage -->
                        {{ getCommentSize }}
                      </div>

                      <div class="mt-2">게시일 : {{ getShareDetail.regdate }}</div>
                    </div>
                  </v-col>
                </v-row>
              </v-sheet>
            </v-sheet>
          </div>

          <!-- 댓글 -->
          <v-container>
            <v-sheet class="mt-10 mb-5">
              <comment-list />
            </v-sheet>
          </v-container>
        </div>
      </v-col>
      <v-col cols="1" md="2">
        <menu-btn
          :board_no="getShareDetail.board_no"
          :title="getShareDetail.title"
          :content="getShareDetail.content"
          :url="getShareDetail.url"
          :content_type="getShareDetail.content_type"
          :nickname="getShareDetail.nickname"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import CommentList from '../../components/shareDetail/CommentList.vue';
import { mapGetters, mapActions } from 'vuex';
import MenuBtn from '../../components/shareDetail/MenuBtn.vue';
import DotMenu from '../../components/shareDetail/DotMenu.vue';
import myVideo from 'vue-video';
import $ from 'jquery';

export default {
  components: { CommentList, MenuBtn, myVideo, DotMenu },

  computed: {
    ...mapGetters('mainStore', ['getShareDetail', 'getCommentSize']),
  },
  data: () => ({
    shareItem: {},
    avatarUrl: '',
    // video: {
    //   options: {
    //     controls: true,
    //     muted: true,
    //     poster: 'https://ifh.cc/g/fP091M.jpg',
    //     autoplay: true,
    //   },
    // },
  }),
  methods: {
    ...mapActions('mainStore', ['findShareDetail', 'updateDetailLike']),
    play() {
      // console.log('동영상 클릭');
    },
    getVideo() {
      return {
        sources: {
          src: this.getShareDetail.url,
          type: 'video/mp4',
        },
      };
    },
    getOption() {
      return {
        options: {
          controls: true,
          muted: true,
          poster: '',
          autoplay: true,
        },
      };
    },
  },
  created() {
    window.scrollTo(0, 0);
    if (this.getShareDetail.board_no == undefined) this.findShareDetail(this.$route.query.no);

    this.avatarUrl = require('../../assets/among' + (Math.floor(Math.random() * 10) + 1) + '.png'); //NOSONAR
  },
  mounted() {
    // appbar 관리
    $('#nav-ul-id').removeClass('main-bar');
    $('#nav-ul-id').addClass('func-bar');
    $('.nav_ul').css('color', 'black');
    $('#navbar').css('background-color', '#ffffff');
    document.getElementsByClassName('__cov-contrl-content')[0].style.zIndex = 1;

    let btn = document.getElementsByClassName('__cov-contrl-play-btn');
    btn[0].click();
  },
};
</script>

<style>
.detail-text {
  padding-bottom: 10px;
  border-bottom: 1px solid rgb(225, 225, 225);
}

.detail-img {
  display: block;
  margin: auto;
}

.back-img {
  background-color: rgb(249, 249, 249);
}

.box-shadow {
  box-shadow: 5px 5px 5px 5px gray;
}

.v-btn--example {
  position: fixed;
}

.menu-choice:hover {
  cursor: pointer;
  color: #3395f4;
}
</style>
