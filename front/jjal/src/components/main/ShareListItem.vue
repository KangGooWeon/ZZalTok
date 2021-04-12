<template>
  <v-row class="mt-4" align="center" justify="center">
    <v-col cols="12">
      <div>
        <div class="figure" @mouseleave="isOverlay = false">
          <v-img
            :src="thumbnail"
            aspect-ratio="1.6"
            class="cur-point share-img2"
            @click="moveDetail()"
            @mouseover="isOverlay = true"
          >
            <div class="img-icon" v-if="content_type=='image'">
              <i class="fas fa-camera"></i> <!-- Compliant icon fonts usage -->
            </div>
            <div class="img-icon" v-if="content_type=='video'">
              <i class="fas fa-play"></i> <!-- Compliant icon fonts usage -->
              </div>
            <div class="img-overlay" v-if="isOverlay">
              <div data-aos="zoom-in" class="overlay-border"> </div>
            </div>
          </v-img>
        </div>

        <div class="ml-1 mt-3">
          <div class="font-weight-bold text-md-body-1">
            <span class="title-choice" @click="moveDetail()">{{ title }}</span>
          </div>
          <div class="font-weight-bold like-lookup mt-1">
            <v-icon small class="mr-1" style="margin-top: -3px"
              >mdi-thumb-up-outline</v-icon
            >
            <span>{{ good }}</span>
            <i class="far fa-eye ml-2"></i> <span>{{ view_cnt }}</span>
            <span>&middot;{{ regdate }}</span>
          </div>
        </div>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import http from "@/util/http-common.js";

export default {
  props: {
    board_no: { Type: Number },
    title: { Type: String },
    content: { Type: String },
    content_type: { Type: String },
    ip: { Type: String },
    good: { Type: Number },
    regdate: { Type: String },
    imageUrl: { Type: String },
    view_cnt: { Type: String },
  },
  data: () => ({
    thumbnail: "",
    isOverlay: false,
  }),
  methods: {
    moveDetail() {
      this.$store
        .dispatch("mainStore/findShareDetail", this.board_no)
        .then((res) => {
          // console.log("이동합니다");
          this.$store.commit('mainStore/SET_IS_SHARE_DETAIL_VIEW', true);
          this.$router.push(`/shareDetail?no=${res}`);
        })
        .catch((error) => {
          console.log("에러", error);
          // console.log("에러내용", error.response);
        });
    },
    findThumbnail() {
      http
        .get(`/v1/thumbnails/${this.board_no}.png`)
        .then(() => {
          this.thumbnail =
            "/api/v1/content/thumbnails/" + this.board_no + ".png";
        })
        .catch((error) => {
          console.log("에러", error);
          // console.log("에러내용", error.response);
        });
    },
  },
  created() {
    this.findThumbnail();
  },
};
</script>

<style>
.figure {
  position: relative;
  overflow: hidden;
  cursor: pointer;
  -webkit-transition: all 0.35s ease;
  transition: all 0.35s ease;
}

.title-choice:hover {
  cursor: pointer;
  border-bottom: 0.5px solid rgb(112, 108, 108);
}

.like-lookup {
  font-size: 13px;
  color: #888888;
}

.img-overlay {
  background: rgba(0, 0, 0, 0.3);
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;

  /* 가운데로 보내는 법 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.overlay-icon {
  color: white;
}
/* 
.img-overlay-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
} */

.share-img2 {
  -webkit-transform: scale(1);
  transform: scale(1);
  -webkit-transition: 0.3s ease-in-out;
  transition: 0.3s ease-in-out;
  border-radius: 4px;
}

.share-img2:hover {
  -webkit-transform: scale(1.3);
  transform: scale(1.3);
}

.img-icon {
  float: right;
  margin-right: 15px;
  margin-top: 10px;
  color: white;
  font-size: 20px;
  filter: drop-shadow(0 0 0.75px rgba(0, 0, 0, 0.42))
    drop-shadow(0 1px 0.5px rgba(0, 0, 0, 0.18))
    drop-shadow(0 2px 3px rgba(0, 0, 0, 0.2));
}

.overlay-border {
  width: 65%;
  height: 65%;
  border: 2px solid white;
}
</style>
