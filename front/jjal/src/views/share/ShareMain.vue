<template>
  <v-container class="main-container back-img" fluid>
    <v-row class="mt-7">
      <v-col cols="12" style="padding:0px">
        <div class="section2 share-img">
          <div class="share-text-body2">
            <div data-aos="fade-up" data-aos-duration="2000" class="share-text">
              <div class="text-xl-h3 text-md-h4 text-h6">
                <span>나만의 밈 공유</span>
              </div>
              <div class="mt-3">
                <span>내가 만든 밈을 공유하고 사람들의 밈을 확인해보세요!</span>
              </div>
            </div>
          </div>
        </div>
      </v-col>
      <v-container>
        <v-row>
          <v-col cols="12">
            <div class="mt-4 ml-5">
              <list-tab />
            </div>
            <v-divider></v-divider>
          </v-col>
          <v-col
            v-for="item in getShareItems"
            :key="item.board_no"
            cols="12"
            sm="6"
            md="4"
            xl="3"
          >
            <share-list-item
              :board_no="item.board_no"
              :title="item.title"
              :content="item.content"
              :content_type="item.content_type"
              :ip="item.ip"
              :good="item.good"
              :regdate="timeForToday(item.regdate)"
              :imageUrl="getUrl(item.content)"
              :thumbnail="item.thumbnail"
              :video="'hi'"
              :view_cnt="item.view_cnt"
            />
          </v-col>

          <v-col cols="12">
            <div style="text-align: center">
              <v-btn text @click="more()" class="mb-5 mt-5"
                ><strong>The More</strong></v-btn
              >
            </div>
          </v-col>
        </v-row>
      </v-container>
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
    movePage: function (move) {
      this.$router.push({ name: move });
    },
    more() {
      this.$store.commit("mainStore/SET_PAGE_COUNT", "more");
      this.fetchShareList(this.getCurrentTab);
    },

    getUrl(str){
      return JSON.parse(str).url
    },

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
  },

  created() {
    window.scrollTo(0, 0);
    //axios하기
    this.$store.commit("mainStore/SET_PAGE_COUNT", "first");
    this.$store.commit("mainStore/SET_SHARE_ITEMS_RESET");
    this.fetchShareList('good');
  },
  
  mounted(){
    $("#nav-ul-id").removeClass("main-bar");
    $("#nav-ul-id").addClass("func-bar");
    $(".nav_ul").css("color", "black");
    $("#navbar").css("background-color", "#ffffff");

    $(".v-slide-group__content").css("text-align", "center");
  }
};
</script>

<style>
.main-container {
  margin-top: -40px;
}

.section2 {
  height: 300px;
  width: 100vw;
  display: table;
  table-layout: fixed;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center center;
}

.share-text-body2 {
  position: absolute;
  padding-top : 100px;
  text-align: center;
  width: 100vw;
}

.back-img {
  background-color: rgb(249, 249, 249);
}
</style>
