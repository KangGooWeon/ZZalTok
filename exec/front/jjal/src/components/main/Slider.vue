<template>
  <v-carousel cycle height="sliderHeight" hide-delimiter-background show-arrows-on-hover>
    <template v-slot:prev="{ on, attrs }">
      <v-btn color="info" v-bind="attrs" v-on="on" fab small>
        <i class="fas fa-chevron-left"></i> <!-- Compliant icon fonts usage -->
      </v-btn>
    </template>
    <template v-slot:next="{ on, attrs }">
      <v-btn color="info" v-bind="attrs" v-on="on" fab small>
        <i class="fas fa-chevron-right"></i> <!-- Compliant icon fonts usage -->
        </v-btn>
    </template>
    <v-carousel-item>
      <v-img :src="require('../../assets/banner1.png')" class="club-image" :aspect-ratio="ratio"></v-img>
    </v-carousel-item>
    <v-carousel-item>
      <v-img :src="require('../../assets/banner2.png')" class="club-image" :aspect-ratio="ratio"></v-img>
    </v-carousel-item>
    <v-carousel-item>
      <v-img :src="require('../../assets/banner3.png')" class="club-image" :aspect-ratio="ratio"></v-img>
    </v-carousel-item>
  </v-carousel>
</template>


<script>
export default {
  computed: {
      ratio () {
        switch (this.$vuetify.breakpoint.name) {
          case 'xs': return 3
          case 'sm': return 3
          case 'md': return 4
          case 'lg': return 5
          case 'xl': return 6
        }
      },

      sliderHeight () {
        switch (this.$vuetify.breakpoint.name) {
          case 'xs': return 120
          case 'sm': return 160
          case 'md': return 200
          case 'lg': return 240
          case 'xl': return 300
        }
      },
    },
  data() {
    return {
      
    };
  },
};
</script>

<style>
.club-image {
  width: 100vw;
  
}
</style>