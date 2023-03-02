<script lang="ts">
import NavBar from "../components/NavBar.vue"
import { defineComponent, h } from "vue";
import { RouterLink, useRoute } from "vue-router";
import type { RouteLocationNormalizedLoaded } from "vue-router";
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
import Contrast from "@vicons/carbon/Contrast"

const menuOptions = [
  {
    to: {
      name: "home",
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
      path: "/time-line",
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
  }
];

export default defineComponent({
  props: {
    changeTheme: {
      type: Function,
      required: true
    }
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
    NavBar
  },
  setup() {
    const route: RouteLocationNormalizedLoaded = useRoute();

    const activeMenu = () => {
      if ((route.path.split("/").length - 1) == 1) {
        route.path.substring(1)
      }
      return route.path.replace(/\//g, ' ').trim().split(' ')[0]
    }

    return {
      menuOptions,
      Contrast,
      route,
      activeMenu
    };
  },
});
</script>

<template>
  <div class="min-h-screen flex flex-col bg-white dark:bg-black dark:text-gray-200">
    <NavBar :menu-options="menuOptions">
      <n-button quaternary circle :focusable="false" @click="changeTheme()">
        <template #icon>
          <n-icon :component="Contrast" />
        </template>
      </n-button>
    </NavBar>
    <main class="grow container xl:max-w-7xl px-4 py-6 lg:py-16 mx-auto">
      <slot />
    </main>
    <footer class="flex justify-between items-center p-6">
      <div>
        <h2>Footer</h2>
      </div>
    </footer>
  </div>
</template>

<style>
.v-binder-follower-container {
  position: initial;
}

.n-layout-header,
.n-layout-footer {
  @apply  h-14 px-4;
}
</style>
