<script lang="ts">
import NavBar from "../components/NavBar.vue";
import Footer from "../components/Footer.vue";
import { useRoute } from "vue-router";
import { NButton, NIcon } from "naive-ui";
import Contrast from "@vicons/carbon/Contrast";

const menuOptions = [
  {
    to: {
      name: "",
      path: "/",
    },
    label: "Home",
    key: "home",
  },
  {
    to: {
      name: "consulta",
      path: "/consulta/lista",
    },
    label: "Consulta",
    key: "consulta",
  },
  {
    to: {
      name: "metodologia",
      path: "/metodologia",
    },
    label: "Metodologia",
    key: "methodology",
  },
  {
    to: {
      name: "timeline",
      path: "/timeline",
    },
    label: "Linha do tempo",
    key: "timeline",
  },
  {
    to: {
      name: "colaborar",
      path: "/colaborar",
    },
    label: "Colaborar",
    key: "collaborate",
  },
  {
    to: {
      name: "sobre",
      path: "/sobre",
    },
    label: "Sobre",
    key: "about",
  },
  {
    to: {
      name: "metamix",
      path: "/metamix",
    },
    label: "Metamix",
    key: "metamix",
  },
];

export default {
  components: {
    NButton,
    NIcon,
    NavBar,
    Footer,
  },
  props: {
    changeTheme: {
      type: Function,
      required: true,
    },
  },
  setup() {
    const route = useRoute();

    return {
      menuOptions,
      Contrast,
      route,
    };
  },
};
</script>

<template>
  <div
    class="min-h-screen flex flex-col bg-white dark:bg-black dark:text-gray-200"
  >
    <NavBar :menu-options="menuOptions">
      <n-button
        quaternary
        circle
        :focusable="false"
        tabindex="0"
        @click="changeTheme()"
      >
        <template #icon>
          <n-icon :component="Contrast" />
        </template>
      </n-button>
    </NavBar>
    <main :class="route.meta.classes ? route.meta.classes : 'grow container-default'">
      <slot />
    </main>
    <Footer />
  </div>
</template>

<style>
/* Resize table rows will break page height fix */
.v-binder-follower-container {
  position: initial;
}

.n-layout-header,
.n-layout-footer {
  @apply h-14 px-4;
}
</style>
