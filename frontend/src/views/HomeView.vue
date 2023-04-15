<script lang="ts">
import { useMeta } from "vue-meta";
import FormSearch from "../components/FormSearch.vue";

export default {
  components: { FormSearch },
  setup() {
    useMeta({
      title: "",
      description: "Tela home do projeto metamemo",
      htmlAttrs: { lang: "pt-br", amp: true },
    });
    return;
  },
};
</script>

<template>
  <section class="dark:text-gray-400 dark:bg-black body-font">
    <div class="container px-5 py-28 mx-auto flex flex-wrap items-center">
      <div class="lg:w-3/5 md:w-1/2 md:pr-16 lg:pr-0 pr-0">
        <h1
          class="title-font font-medium text-3xl text-gray-800 dark:text-white"
        >
          <span class="font-bold">METAMEMO</span> é um sistema criado para
          coletar, armazenar e visualizar as memórias de qualquer pessoa (ou
          organização, coletivo, empresa, marca).
        </h1>
      </div>
      <div
        class="lg:w-2/6 md:w-1/2 bg-slate-100 dark:bg-slate-900 rounded-lg p-8 flex flex-col md:ml-auto w-full mt-10 md:mt-0"
      >
        <h2 class="dark:text-white text-lg font-medium title-font mb-5">
          Busque um <span class="font-bold">METAMEMO</span>
        </h2>
        <FormSearch :display-tabs="false" />
      </div>
    </div>
  </section>
</template>
