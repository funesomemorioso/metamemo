<script lang="ts">
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
import type { MenuOption } from "naive-ui"
import Contrast from "@vicons/carbon/Contrast"

const menuOptions: MenuOption[] = [
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: "home",
            path: "/",
          },
        },
        { default: () => "Home" }
      ),
    key: "home",
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            path: "/methodology",
          },
        },
        { default: () => "Metodologia" }
      ),
    key: "methodology",
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            path: "/query",
          },
        },
        { default: () => "Consulta" }
      ),
    key: "query",
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            path: "/time-line",
          },
        },
        { default: () => "Linha do Tempo" }
      ),
    key: "time-line",
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            path: "/collaborate",
          },
        },
        { default: () => "Colabore" }
      ),
    key: "collaborate",
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: "about",
          },
        },
        { default: () => "Sobre" }
      ),
    key: "about",
  },
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
    Contrast
  },
  setup() {
    const route: RouteLocationNormalizedLoaded = useRoute();

    return {
      menuOptions,
      Contrast,
      route,
    };
  },
});
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <n-layout-header
      bordered
      class="flex justify-between items-center"
    >
      <div> </div>
      <n-menu
        mode="horizontal"
        :value="route.path.substring(1)"
        :options="menuOptions"
      />
      <n-button quaternary circle :focusable="false" @click="changeTheme()">
        <template #icon>
          <n-icon :component="Contrast" />
        </template>
      </n-button>
    </n-layout-header>
    <n-layout-content class="p-12 grow">
      <slot />
    </n-layout-content>
    <n-layout-footer class="flex justify-between items-center" bordered>
      <div>
        <h2>Footer</h2>
      </div>
    </n-layout-footer>
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
