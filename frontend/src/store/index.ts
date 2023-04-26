import { createStore } from "vuex";

const getDefaultState = () => {
  return {
    form: {
      dateRange: null,
      socialMedia: [],
      selectedPeople: [],
      searchText: "",
    },
    modalPost: {
      showModal: false,
      content: [],
      test: "",
    },
    tab: "lista",
    pageSize: 20,
    page: 1,
    pageSizes: [10, 20, 30, 50, 100],
    sorter: null,
  };
};

// New instance store
export default createStore({
  state() {
    return getDefaultState();
  },
  mutations: {
    UPDATE_FORM(state, payload) {
      state.form = payload;
    },
    UPDATE_TAB(state, payload) {
      // Update tab will reset some state fields
      state.page = 1;
      state.sorter = null;
      state.form.socialMedia = [];
      state.form.selectedPeople = [];
      state.tab = payload;
    },
    UPDATE_PAGE(state, payload) {
      state.page = payload;
    },
    UPDATE_PAGE_SIZE(state, payload) {
      state.page = 1;
      state.pageSize = payload;
    },
    UPDATE_SORTER(state, payload) {
      state.page = 1;
      state.sorter = payload;
    },
    UPDATE_FROM_URL(state, payload) {
      Object.assign(state, payload);
    },
    UPDATE_POST_MODAL(state, payload) {
      state.modalPost = payload;
    },
    SHOW_POST_MODAL(state, payload) {
      state.modalPost.showModal = payload;
    },
    CLEAN_STATE(state) {
      Object.assign(state, getDefaultState());
    },
  },
});
