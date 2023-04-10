<script lang="ts">
import {
  NConfigProvider,
  NMessageProvider,
  darkTheme,
  ptBR,
  datePtBR,
} from "naive-ui";
import { defineComponent, ref, onBeforeMount} from "vue";

import type { GlobalThemeOverrides } from "naive-ui";
import type { Ref } from "vue";

export default defineComponent({
  components: { NConfigProvider, NMessageProvider },
  setup() {
    const SITE_NAME = "Metamemo";
    let darkThemed: boolean = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;
    const theme: Ref = ref(null);

    const lightThemeOverrides: GlobalThemeOverrides = {
      common: {
        primaryColor: "#ef5da8",
        primaryColorHover: "#bd4a85",
      },
    };

    const darkThemeOverrides: GlobalThemeOverrides = {
      common: {
        primaryColor: "#ef5da8",
        primaryColorHover: "#bd4a85",
      },
    };

    const setTheme = () => {
      if (darkThemed) {
        theme.value = darkTheme;
        document.documentElement.classList.add("dark");
      } else {
        theme.value = null;
        document.documentElement.classList.remove("dark");
      }
    };

    onBeforeMount(() => {
      setTheme();
    });

    const changeTheme = () => {
      darkThemed = !darkThemed;
      setTheme();
    };

    return {
      theme,
      changeTheme,
      lightThemeOverrides,
      darkThemeOverrides,
      SITE_NAME,
      ptBR,
      datePtBR,
    };
  },
});
</script>

<template>
  <metainfo>
    <template v-slot:title="{ content }">
      {{ content ? `${content} | ${SITE_NAME}` : SITE_NAME }}
    </template>
  </metainfo>
  <div id="app">
    <n-config-provider
      :theme-overrides="
        theme === null ? lightThemeOverrides : darkThemeOverrides
      "
      :theme="theme"
      :locale="ptBR"
      :date-locale="datePtBR"
    >
      <n-message-provider>
        <AppLayout :changeTheme="changeTheme">
          <router-view />
        </AppLayout>
      </n-message-provider>
    </n-config-provider>
  </div>
</template>
