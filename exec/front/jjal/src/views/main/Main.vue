<template>
  <v-container style="padding: 0px; margin-top: -92px" fluid>
    <v-row>
      <v-col cols="12">
        <div class="section share-img">
          <div class="share-text-body">
            <div data-aos="fade-up" data-aos-duration="2000" class="share-text">
              <div class="text-xl-h3 text-md-h4 text-h6">
                <span>나만의 밈 공유</span>
              </div>
              <div class="mt-3">
                <span>내가 만든 밈을 공유하고 사람들의 밈을 확인해보세요!</span>
              </div>
              <div>
                <v-btn
                  class="mt-3"
                  outlined
                  dark
                  large
                  @click="movePage('ShareMain')"
                  >바로가기</v-btn
                >
              </div>
            </div>
          </div>
        </div>
      </v-col>

      <v-col cols="6" class="hidden-md-and-down">
        <div data-aos="zoom-in" data-aos-duration="2000" class="main-text">
          <div class="text-xl-h3 text-md-h4 text-h6 height-medi">
            <span>얼굴 체인지</span>
          </div>
          <i class="far fa-laugh-squint"></i> <!-- Compliant icon fonts usage -->
          <div class="mt-3">원하는 인물과 자신의 사진을 합성해보세요!</div>
          <v-btn class="mt-3" rounded outlined large color="#ff5757" @click="movePage('DeepFakeImage')"
            >바로가기</v-btn
          >
        </div>
      </v-col>

      <v-col cols="12" lg="6">
        <div data-aos="fade-up" data-aos-duration="2000" class="mr-5">
          <v-img
            :src="require('../../assets/1.png')"
            class=""
            width="1260px"
            height="950px"
            style="float: right"
            ><div class="main-img-text hidden-lg-and-up">
              <div class="text-xl-h3 text-md-h4 text-h6">
                <span>얼굴 체인지</span>
              </div>
              <div class="mt-3">
                <span>원하는 인물과 자신의 사진을 합성해보세요!</span>
              </div>
              <div>
                <v-btn class="mt-3" rounded outlined dark large  @click="movePage('DeepFakeImage')">바로가기</v-btn>
              </div>
            </div>
          </v-img>
        </div>
      </v-col>

      <v-col cols="12" lg="6">
        <div
          data-aos="fade-right"
          data-aos-easing="ease-in-sine"
          data-aos-duration="2000"
          class="ml-5"
        >
          <v-img
            :src="require('../../assets/2.png')"
            class=""
            width="1260px"
            height="950px"
            ><div class="main-img-text hidden-lg-and-up">
              <div class="text-xl-h3 text-md-h4 text-h6">
                <span>다메다메 영상</span>
              </div>
              <div class="mt-3">
                <span
                  >핫한 다메다메 아저씨 영상에 자신의 얼굴을 넣어보세요!</span
                >
              </div>
              <div>
                <v-btn class="mt-3" rounded outlined dark large @click="movePage('DeepFakeMovie')">바로가기</v-btn>
              </div>
            </div></v-img
          >
        </div>
      </v-col>
      <v-col cols="6" class="hidden-md-and-down">
        <div
          data-aos="zoom-in-down"
          data-aos-duration="2000"
          class="main-text2"
        >
          <div class="text-xl-h3 text-md-h4 text-h6 height-medi">
            <span>다메다메 영상</span>
          </div>
          <div class="mt-3">
            핫한 다메다메 아저씨 영상에 자신의 얼굴을 넣어보세요!
          </div>
          <v-btn class="mt-3" rounded outlined large color="#d4bdad" @click="movePage('DeepFakeMovie')"
            >바로가기</v-btn
          >
        </div>
      </v-col>

      <v-col cols="6" class="hidden-md-and-down">
        <div data-aos="flip-left" data-aos-duration="2000" class="main-text3">
          <div class="text-xl-h3 text-md-h4 text-h6 height-medi">
            <span>나만의 배경</span>
          </div>
          <div class="mt-3">원하는 동영상에 배경을 바꾸고 싶다면?</div>
          <v-btn
            class="mt-3"
            rounded
            outlined
            large
            color="#fce9b5"
            @click="movePage('RemoveBack')"
            >바로가기</v-btn
          >
        </div>
      </v-col>

      <v-col cols="12" lg="6">
        <div data-aos="fade-left" data-aos-duration="2000" class="mr-5">
          <v-img
            :src="require('../../assets/3.png')"
            width="1260px"
            height="950px"
            ><div class="main-img-text hidden-lg-and-up">
              <div class="text-xl-h3 text-md-h4 text-h6">
                <span>나만의 배경</span>
              </div>
              <div class="mt-3">
                <span>원하는 동영상에 배경을 바꾸고 싶다면?</span>
              </div>
              <div>
                <v-btn class="mt-3" rounded outlined dark large @click="movePage('RemoveBack')">바로가기</v-btn>
              </div>
            </div></v-img
          >
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import VueSlickCarousel from "vue-slick-carousel";
import "vue-slick-carousel/dist/vue-slick-carousel.css";
import "vue-slick-carousel/dist/vue-slick-carousel-theme.css";
import ShareListItem from "../../components/main/ShareListItem.vue";
import { mapGetters, mapActions } from "vuex";
import Slider from "../../components/main/Slider.vue";
import ListTab from "../../components/main/ListTab.vue";
import $ from "jquery";

export default {
  components: { VueSlickCarousel, ShareListItem, Slider, ListTab },
  computed: {
    ...mapGetters("mainStore", ["getShareItems", "getCurrentTab"]),
  },
  data: () => ({
    drawer: null,

    slickData: {
      slidesToShow: 1,
      slidesToScroll: 1,
      speed: 400,
      autoplay: true,
      arrows: false,
      autoplaySpeed: 2000,
      responsive: [
        { breakpoint: 1600, settings: { slidesToShow: 1, slidesToScroll: 1 } },
        { breakpoint: 1200, settings: { slidesToShow: 1, slidesToScroll: 1 } },
        { breakpoint: 750, settings: { slidesToShow: 1, slidesToScroll: 1 } },
      ],
    },

    items: {},
  }),
  methods: {
    ...mapActions("mainStore", ["fetchShareList"]),
    movePage(move) {
      this.$router.push({ name: move });
      this.$store.commit("SET_ON_OFF_MENU", false);
    },
  },

  created() {
    window.scrollTo(0, 0);

    // appbar 관리
    // console.log("여기???");
    $("#nav-ul-id").addClass("main-bar");
    $("#nav-ul-id").removeClass("func-bar");
    $("#navbar").css("background-color", "rgba( 255, 255, 255, 0 )");
    $(".nav_ul").css("color", "white");
  },
};
</script>

<style>
.main-container {
  margin-top: -40px;
}

.back-img {
  background-color: rgb(249, 249, 249);
}

.section {
  height: 1000px;
  width: 100vw;
  display: table;
  table-layout: fixed;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center center;
}
.share-img {
  background-image: url("../../assets/share.png");
}

.share-text {
  color: white;
  /* transform: translate(-40%, -50%); */
  text-align: center;
}

.share-text-body {
  position: absolute;
  top: 7%;
  text-align: center;
  width: 100vw;
}

.main-text {
  text-align: center;
  color: #ff5757;
  height: 1000px;
  font-weight: bold;
}

.main-text2 {
  text-align: center;
  color: #d4bdad;
  height: 1000px;
  font-weight: bold;
}

.main-text3 {
  text-align: center;
  color: #fce9b5;
  height: 1000px;
  font-weight: bold;
}

.height-medi {
  height: 480px;
  padding-top: 430px;
}

.main-img-text {
  color: white;
  text-align: center;
  height: 1000px;
  padding-top: 400px;
}
</style>