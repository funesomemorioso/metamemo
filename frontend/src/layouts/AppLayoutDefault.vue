<script lang="ts">
import NavBar from "../components/NavBar.vue";
import Footer from "../components/Footer.vue";
import { useRoute } from "vue-router";
import {
  NLayout,
  NLayoutHeader,
  NLayoutContent,
  NLayoutFooter,
  NMenu,
  NButton,
  NSpace,
  NAnchorLink,
  NIcon,
} from "naive-ui";
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
      name: "methodology",
      path: "/methodology",
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
      name: "collaborate",
      path: "/collaborate",
    },
    label: "Colaborar",
    key: "collaborate",
  },
  {
    to: {
      name: "about",
      path: "/about",
    },
    label: "Sobre",
    key: "about",
  },
];

export default {
  props: {
    changeTheme: {
      type: Function,
      required: true,
    },
  },
  components: {
    NLayout,
    NLayoutHeader,
    NLayoutContent,
    NLayoutFooter,
    NMenu,
    NButton,
    NSpace,
    NAnchorLink,
    NIcon,
    Contrast,
    NavBar,
    Footer,
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
        @click="changeTheme()"
        tabindex="0"
      >
        <template #icon>
          <n-icon :component="Contrast" />
        </template>
      </n-button>
    </NavBar>
    <main class="grow container-default" :class="route.meta.classes">
      <slot />
    </main>
    <Footer />
  </div>
</template>

<style>
.v-binder-follower-container {
  position: initial;
}

.n-layout-header,
.n-layout-footer {
  @apply h-14 px-4;
}
</style>
