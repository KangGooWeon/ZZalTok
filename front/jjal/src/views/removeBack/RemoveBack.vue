<template>
  <RemoveBack></RemoveBack>
</template>

<script>
import RemoveBack from '@/components/removeBack/MakeRemoveBack.vue';
import $ from "jquery";
export default {
  components: { RemoveBack },
  mounted(){
    // appbar 관리
    // console.log("왜 안되지")
    window.scrollTo(0,0);
    $("#nav-ul-id").removeClass("main-bar");
    $("#nav-ul-id").addClass("func-bar");
    $(".nav_ul").css("color", "black");
    $("#navbar").css("background-color", "#ffffff");
  }
};
</script>
