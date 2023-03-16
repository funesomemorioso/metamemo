<script lang="ts">
import { RouterView } from "vue-router";
import { NConfigProvider, darkTheme, ptBR, datePtBR } from "naive-ui";
import { defineComponent, ref } from "vue";

import type { GlobalThemeOverrides, GlobalTheme } from "naive-ui";
import type { Ref } from "vue";

export default defineComponent({
  components: { darkTheme, NConfigProvider, ptBR, datePtBR },
  setup() {
    const SITE_NAME = "Metamemo";
    let darkThemed: boolean = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;
    const theme: { value: GlobalTheme } | Ref = ref(
      darkThemed ? darkTheme : null
    );

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

    const changeTheme: Function = () => {
      darkThemed = !darkThemed;

      if (darkThemed) {
        theme.value = darkTheme;
      } else {
        theme.value = null;
      }
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
      :class="theme ? 'dark' : ''"
    >
      <AppLayout :changeTheme="changeTheme">
        <router-view />
      </AppLayout>
    </n-config-provider>
  </div>
</template>
