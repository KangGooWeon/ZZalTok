<template>
  <v-navigation-drawer v-model="getDrawer" absolute temporary right width="30vh" height="100vh" style="position : fixed">
    <v-list dense style="font-size:20px">
      <v-list-item v-for="item in items" :key="item.title" link @click="movePage(item.name)">
        <v-list-item-icon class="mt-4">
          <i :class="item.icon"></i> <!-- Compliant icon fonts usage -->
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title style="padding-top:6px; font-size:15px">
            <span class="font-we">{{ item.title }}</span>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <!-- 배경누르면 창 꺼지게 -->
    <button style="display: none" id="chagemenu" @click="OnOffMenu">ddd</button>
  </v-navigation-drawer>
</template>

<script>
import $ from 'jquery';

export default {
  computed: {
    getDrawer: {
      get: function () {
        return this.$store.getters.isOnOffMenu;
      },
      set: function () {},
    },
  },
  data() {
    return {
      items: [
        { title: '홈으로', icon: 'fas fa-home', name: 'Main' },
        { title: '얼굴 체인지', icon: 'fas fa-smile', name: 'DeepFakeImage' },
        { title: '다메다메', icon: 'fas fa-microphone pl-1', name: 'DeepFakeMovie' },
        { title: '나만의 배경', icon: 'fas fa-images', name: 'RemoveBack' },
        { title: '밈 공유', icon: 'fas fa-share-square', name: 'ShareMain' },
      ],
      nickname: '',
    };
  },
  updated() {
    // 바탕화면 누르면 vuex 값을 바꿔주기 위해
    $(document).ready(function () {
      $('.v-overlay').on('click', function () {
        $('#chagemenu').trigger('click');
      });
    });
  },
  methods: {
    movePage: function (move) {
      this.OnOffMenu();
      this.$router.push({ name: move });
    },
    OnOffMenu: function () {
      this.$store.commit('SET_ON_OFF_MENU', false);
    },
  },
};
</script>

<style>
.menu-title{
  background-color: gray;
}
</style>
