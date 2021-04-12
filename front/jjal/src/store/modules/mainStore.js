import http from "@/util/http-common.js";

const mainStore = {
  namespaced: true,
  state: {
    shareItems: [],
    shareDetail: {},
    isShareDetailView: false,
    pageCount: 1,
    currentTab: 'good',

    //댓글
    commentItems: {},
    commentSize: {},
  },
  getters: {
    getShareItems(state) {
      return state.shareItems;
    },
    getShareDetail(state) {
      return state.shareDetail;
    },
    getIsShareDetailView(state){
      return state.isShareDetailView;
    },
    getPageCount(state){
      return state.pageCount;
    },
    getCurrentTab(state){
      return state.currentTab;
    },
    getCommentItems(state) {
      return state.commentItems;
    },
    getCommentSize(state) {
      return state.commentSize;
    },
  },
  mutations: {
    SET_SHARE_ITEMS(state, payload) {
      for (let i = 0; i < payload.length; i++) {
        state.shareItems.push(payload[i]);
      }
    },
    SET_SHARE_ITEMS_RESET(state) {
      state.shareItems = [];
    },

    SET_SHARE_DETAIL(state, payload) {
      state.shareDetail = payload;
      state.shareDetail.regdate = state.shareDetail.regdate.replace("T", " ").substr(0, 16);
      state.shareDetail.url = JSON.parse(state.shareDetail.content).url;
      state.shareDetail.content = JSON.parse(state.shareDetail.content).content;
    },

    SET_IS_SHARE_DETAIL_VIEW(state, payload){
      state.isShareDetailView = payload;
    },
    SET_PAGE_COUNT(state, payload){
      if(payload == 'first') state.pageCount = 1;
      else state.pageCount += 1;
    },
    SET_COMMENT_ITEMS(state, payload) {
      state.commentItems = payload;
      state.commentSize = Object.keys(payload).length;
    },
    SET_CURRENT_TAB(state, payload){
      state.currentTab = payload;
    },
  },
  actions: {
    //공유짤 조회 추천순
    async fetchShareList({ commit, state }, str) {
      await http
        .get(`/v1/board/${str}`, { params: { page_count: state.pageCount } })
        .then((res) => {
          // console.log("공유 최신순 불러오기 성공");
          commit("SET_SHARE_ITEMS", res.data.items);
        })
        .catch((error) => {
          console.log("에러", error);
          console.log("에러내용", error.response);
        });
    },

    //공유 디테일
    async findShareDetail({ commit, dispatch }, no) {
      let board_no = 0;
      await http
        .get(`/v1/board/detail/${no}`)
        .then((res) => {
          // console.log("공유 디테일 불러오기 성공");
          commit("SET_SHARE_DETAIL", res.data);
          dispatch("fetchCommentList", res.data.board_no);
          board_no = res.data.board_no;
        })
        .catch((error) => {
          console.log("에러", error);
          console.log("에러내용", error.response);
        });
        
        return board_no;
    },

    //게시물 수정
    updateShareDetail({ dispatch, state }, data) {
      http
        .put(`/v1/board/${data.board_no}`, data)
        .then(() => {
          // console.log("공유 디테일 수정 성공");
          dispatch("findShareDetail", state.shareDetail.board_no);
        })
        .catch((error) => {
          console.log("에러", error);
          console.log("에러내용", error.response);
        });
    },

    //게시물 삭제
    deleteShareDetail({ dispatch }, data) {
      http
        .delete(`/v1/board/${data.no}`, { params: { password: data.password } })
        .then(() => {
          // console.log("게시물 삭제 성공");
          dispatch("fetchShareList");
        })
        .catch((error) => {
          console.log("에러", error);
          console.log("에러내용", error.response);
        });
    },

    //댓글 불러오기
    fetchCommentList({ commit }, no) {
      http
        .get(`/v1/comment/${no}`)
        .then((res) => {
          // console.log("댓글 조회 불러오기 성공");
          commit("SET_COMMENT_ITEMS", res.data);
        })
        .catch((error) => {
          console.log("에러", error);
          console.log("에러내용", error.response);
        });
    },

    //댓글 등록
    createComment({ dispatch }, data) {
      http
        .post(`/v1/comment/write/${data.no}`, data.item)
        .then((res) => {
          // console.log("댓글 등록 성공");
          dispatch("fetchCommentList", data.no);
        })
        .catch((error) => {
          console.log("에러", error);
          console.log("에러내용", error.response);
        });
    },

    updateComment({ dispatch, state }, data) {
      http
        .put(
          `/v1/comment/${data.no}?content=${data.content}&nickname=${data.nickname}&password=${data.password}`
        )
        .then((res) => {
          // console.log(res);
          dispatch("fetchCommentList", state.shareDetail.board_no);
        })
        .catch((error) => {
          console.log("에러", error);
          console.log("에러내용", error.response);
        });
    },

    deleteComment({ dispatch, state }, data) {
      // console.log(data.password);
      http
        .delete(`/v1/comment/${data.no}`, { params: { password: data.password } })
        .then(() => {
          // console.log("댓글 삭제 성공");
          dispatch("fetchCommentList", state.shareDetail.board_no);
        })
        .catch((error) => {
          console.log("에러", error);
          console.log("에러내용", error.response);
        });
    },

    //좋아요 기능
    updateDetailLike({ dispatch, state }, no) {
      http
        .post(`/v1/board/like/${no}`)
        .then((res) => {
          // console.log(res.data);
          dispatch("findShareDetail", state.shareDetail.board_no);
        })
        .catch((error) => {
          console.log("에러", error);
          console.log("에러내용", error.response);
        });
    },
  },
};

export default mainStore;
