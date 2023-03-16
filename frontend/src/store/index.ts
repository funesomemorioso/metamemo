import { createStore } from "vuex";

const getDefaultState = () => {
  return {
    form: {
      dateRange: null,
      socialMedia: [],
      selectedPeople: [],
      searchText: "",
    },
    tab: "lista",
    pageSize: 10,
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
      state.page = 1;
      state.sorter = null;
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
    CLEAN_STATE(state) {
      Object.assign(state, getDefaultState());
    },
  },
});
