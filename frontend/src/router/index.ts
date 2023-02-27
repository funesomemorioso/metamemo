import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import QueryView from "../views/QueryView.vue";
import MethodologyView from "../views/MethodologyView.vue";
import TimeLineView from "../views/TimeLineView.vue";
import CollaborateView from "../views/CollaborateView.vue";
import AboutView from "../views/AboutView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "",
      name: "home",
      component: HomeView,
    },
    {
      path: "/methodology",
      name: "methodology",
      component: MethodologyView,
    },
    {
      path: "/query",
      name: "query lista",
      component: QueryView,
    },
    {
      path: "/time-line",
      name: "time-line",
      component: TimeLineView,
    },
    {
      path: "/collaborate",
      name: "collaborate",
      component: CollaborateView,
    },
    {
      path: "/about",
      name: "about",
      component: AboutView,
    },
  ],
});

export default router;
