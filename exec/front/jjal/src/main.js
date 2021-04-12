import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import VueHtml2Canvas from 'vue-html2canvas';
import VueSimpleAlert from "vue-simple-alert";
import 'regenerator-runtime/runtime';
import AOS from 'aos';
import 'aos/dist/aos.css';

Vue.use(VueSimpleAlert);
Vue.use(VueHtml2Canvas);
Vue.use(vuetify);
Vue.config.productionTip = false;
Vue.AOS = new AOS.init({ disable: 'phone' });

Kakao.init('ddb623655a870366ed7cf4d06b01c92a'); // Kakao init

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
