<template>
  <v-app class="" id="app">
    <navigation />
    <menuBar />

    <v-main class="main-back">
      <router-view />
    </v-main>

    <footerBar />
  </v-app>
</template>

<script>
import Navigation from "./components/common/Navigation.vue";
import MenuBar from "./components/common/MenuBar.vue";
import FooterBar from "./components/common/Footer.vue";
import $ from "jquery";

export default {
  name: "App",
  components: { Navigation, MenuBar, FooterBar },
  created() {
    $(window).scroll(function (e) {
      // 메인페이지 클래스 존재할 시
      if ($('#nav-ul-id').hasClass("main-bar")) {
        if ($(document).scrollTop() > 980) {
          // console.log("메인페이지 980이상");
          $(".nav_ul").css("color", "black");
          $("#navbar").css("background-color", "#ffffff");
          $('.v-toolbar__content').css('box-shadow','0 0 6px 2px rgb(0 0 0 / 16%)');
        } else {
          // console.log("메인페이지 밈 공유");
          $('.v-toolbar__content').css('box-shadow','');
          $("#navbar").css("background-color", "rgba( 255, 255, 255, 0 )");
          $(".nav_ul").css("color", "white");
        }
      }

      // 메인페이지가 아닐시
      if ($('#nav-ul-id').hasClass("func-bar")){
        if ($(document).scrollTop() !=0 ) {
          $('.v-toolbar__content').css('box-shadow','0 0 6px 2px rgb(0 0 0 / 16%)');
        } else {
           $('.v-toolbar__content').css('box-shadow','');
        }
      }
    });
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding&display=swap");

.font-we {
  font-weight: 600;
}

.cur-point {
  cursor: pointer;
}

#app,
span {
  font-family: "Nanum Gothic Coding", monospace;
}

.main-back {
  padding: 0px;
}
</style>
