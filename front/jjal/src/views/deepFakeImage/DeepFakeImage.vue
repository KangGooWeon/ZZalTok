<template>
  <div>
    <DeepFakeImage></DeepFakeImage>
  </div>
</template>

<script>
import DeepFakeImage from "@/components/deepFakeImage/MakeDeepFakeImage.vue";
import $ from "jquery";

export default {
  components: { DeepFakeImage },
  mounted() {
    // appbar 관리
    window.scrollTo(0,0);
    // console.log("dddddd")
    $("#nav-ul-id").removeClass("main-bar");
    $("#nav-ul-id").addClass("func-bar");
    $(".nav_ul").css("color", "black");
    $("#navbar").css("background-color", "#ffffff");
  },
};
</script>
