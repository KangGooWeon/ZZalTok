import Vue from "vue";
import Vuex from "vuex";
import mainStore from "./modules/mainStore";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    //MenuBar OnOff 정보
    on_off_menu : false,

    //이용약관 dialog
    is_agreement_to_terms : false,
  },
  getters:{
    isOnOffMenu(state){
      return state.on_off_menu;
    },
    isAgreementToTerms(state){
      return state.is_agreement_to_terms;
    }
  },
  mutations: {
    SET_ON_OFF_MENU(state, check){
      state.on_off_menu = check;
    },
    SET_IS_AGREEMENT_TO_TERMS(state, payload){
      state.is_agreement_to_terms = payload;
    }
  },
  actions: {
    
  },
  modules: {
    mainStore : mainStore,
  },
});
