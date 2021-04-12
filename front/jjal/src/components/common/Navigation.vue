<template>
  <v-app-bar app color="" flat id="navbar" height="80vh" class="test">
    <img
      :src="require('../../assets/Nav_Logo.png')"
      class="nav-choice ml-5"
      @click="movePage('Main')"
      style="height: 80px"
    />

    <ul class="nav_ul hidden-sm-and-down main-bar" id="nav-ul-id" style="color:white">
      <li class="nav_title nav-choice" @click="movePage('DeepFakeImage')">얼굴 체인지</li>
      <li class="nav_title nav-choice" @click="movePage('DeepFakeMovie')">다메다메</li>
      <li class="nav_title nav-choice" @click="movePage('RemoveBack')">나만의 배경</li>
      <li class="nav_title nav-choice" @click="movePage('ShareMain')">밈 공유</li>
    </ul>

    <v-spacer></v-spacer>

    <v-app-bar-nav-icon class="hidden-md-and-up menu-bar" @click="OnOffMenu"></v-app-bar-nav-icon>
  </v-app-bar>
</template>

<script>
export default {
  data() {
    return { drawer: null };
  },
  methods: {
    movePage: function (move) {
      this.$router.push({ name: move });
      this.$store.commit('SET_ON_OFF_MENU', false);
    },
    OnOffMenu() {
      this.$store.commit('SET_ON_OFF_MENU', true);
    },
  },
  
};
</script>

<style>
#navbar{
  background-color: #ffffff;
  background-color: rgba( 255, 255, 255, 0 );
}

ul li {
  list-style-type: none;
  float: left;
  margin: 20px;
  font-weight: 600;
}

.nav-choice:hover {
  cursor: pointer;
  color: #3395f4;
}

</style>
