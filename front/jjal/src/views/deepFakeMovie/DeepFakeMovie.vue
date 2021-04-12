<template>
  <div>
    <DeepFakeMovie></DeepFakeMovie>
  </div>
</template>

<script>
import DeepFakeMovie from '@/components/deepFakeMovie/MakeDeepFakeMovie.vue';
import $ from "jquery";
export default {
  components: { DeepFakeMovie },
  mounted(){
        // appbar 관리
    window.scrollTo(0,0);
    $("#nav-ul-id").removeClass("main-bar");
    $("#nav-ul-id").addClass("func-bar");
    $(".nav_ul").css("color", "black");
    $("#navbar").css("background-color", "#ffffff");
  }
};
</script>
