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
      path: "/consulta/lista/",
      name: "consulta lista",
      component: QueryView,
    },
    {
      path: "/consulta/news/",
      name: "consulta noticias",
      component: QueryView,
    },
    {
      path: "/consulta/contexts/",
      name: "consulta contexto",
      component: QueryView,
    },
    {
      path: "/consulta/newscovers/",
      name: "consulta capas de jornais",
      component: QueryView,
    },
    {
      path: "/consulta/transcricao/",
      name: "consulta transcicao",
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
