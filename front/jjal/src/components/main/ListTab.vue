<template>
  <v-tabs background-color="rgb(249, 249, 249)">
    <v-tab style="color: #8e8e8e" @click="changeTeb('good')">
      <i class="fas fa-thumbs-up mr-2"></i> <!-- Compliant icon fonts usage -->
      추천순</v-tab
    >
    <v-tab style="color: #8e8e8e" @click="changeTeb('view')">
      <i class="fas fa-eye mr-2"></i> <!-- Compliant icon fonts usage -->
      조회순</v-tab
    >
    <v-tab style="color: #8e8e8e" @click="changeTeb('newest')">
      <i class="fas fa-upload mr-2"></i> <!-- Compliant icon fonts usage -->
      최신순</v-tab
    >
  </v-tabs>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data: () => ({}),
  methods: {
    ...mapActions("mainStore", [
      "fetchShareList",
    ]),
    changeTeb(str) {
      this.$store.commit("mainStore/SET_PAGE_COUNT", "first");
      this.$store.commit("mainStore/SET_CURRENT_TAB", str);
      this.$store.commit("mainStore/SET_SHARE_ITEMS_RESET");

      this.fetchShareList(str);
    },
  },
};
</script>
