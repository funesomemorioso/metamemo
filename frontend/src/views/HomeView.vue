<script lang="ts">
import { useMeta } from "vue-meta";
import FormSearch from "../components/FormSearch.vue";
import bgFam from "../assets/imgs/familia-bolsonaro.png";

export default {
  components: { FormSearch },
  setup() {
    useMeta({
      title: "",
      description: "Tela home do projeto metamemo",
      htmlAttrs: { lang: "pt-br", amp: true },
    });

    const redirectToBlog = () => window.open(import.meta.env.VITE_BLOG_LINK);

    return { redirectToBlog, bgFam };
  },
};
</script>

<template>
  <section class="dark:text-gray-400 dark:bg-black body-font">
    <div class="container mx-auto px-8 2xl:px-32 flex flex-col xl:flex-row py-24 gap-20">
      <article class="flex items-center">
        <h1
          class="text-2xl text-gray-800 dark:text-white"
        >
          <strong>METAMEMO</strong> é um sistema criado para
          coletar, armazenar e visualizar as memórias de qualquer pessoa (ou
          organização, coletivo, empresa, marca).
        </h1>
      </article>
      <div
        class="bg-slate-100 dark:bg-slate-900 rounded-lg p-8 flex flex-col lg:w-5/6 w-full mx-auto"
      >
        <h2 class="dark:text-white text-lg font-medium title-font mb-5">
          Busque um <span class="font-bold">METAMEMO</span>
        </h2>
        <FormSearch :display-tabs="false" />
      </div>
    </div>
  </section>
  <section class="bg-gradient-to-r from-cyan-600 to-blue-700 dark:from-cyan-700 dark:to-blue-800">
    <article class="pt-24 pb-24 space-y-8 container-text text-white">
      <h1 class="header-1">O que é o METAMEMO?</h1>
      <p class="text-lg">METAMEMO é um sistema criado para coletar, armazenar e visualizar as memórias de qualquer pessoa nas mais populares plataformas de redes sociais da internet. O objetivo é preservar e facilitar a análise desse conteúdo por parte de ativistas, jornalistas e pesquisadores.</p>
      <p class="text-lg">Um METAMEMO é um arquivo contendo um arquivo das redes sociais e suas respectivas mídias agregadas de uma pessoa/coletivo/empresa/marca.</p>
      <button
        class="btn"
        onclick="window.location = `/metodologia`"
      >Saiba mais</button>
    </article>
  </section>
  <section class="flex flex-col xl:flex-row">
    <div class="bg-gradient-to-r from-gray-400 to-transparent dark:from-gray-500 lg:min-h-full flex-1 flex items-end justify-center">
      <div class="md:pt-24">
        <img :src="bgFam" alt="Família bolsonaro" />
      </div>
    </div>
    <article class="flex-1 flex items-center">
      <div class="mx-auto px-8 py-32 space-y-12">
        <h1 class="header-1 text-gray-800">Linha do tempo Bolsodata</h1>
        <p class="text-gray-800 font-semibold dark:text-gray-300">
          Selecione um personagem e navegue pela tempo. Acompanhe o histórico de notícias relativos a cada dia em que dados relevantes foram adicionados na base do Metamemo.
        </p>
        <button
          class="btn"
          onclick="window.location = `/timeline`"
        >Acessar</button>
        </div>
    </article>
  </section>
  <section class="bg-gradient-to-r from-green-600 to-cyan-700 dark:from-green-700 dark:to-cyan-800">
    <article class="py-32 space-y-8 container-text text-gray-700 dark:text-gray-200 text-white">
      <h1 class="header-1">Metamix</h1>
      <p class="text-lg">MetaMix é um blog com produções criadas através da nossa plataforma</p>
      <button class="btn" :onclick="redirectToBlog">Acessar</button>
    </article>
  </section>
  <section>
    <article class="py-32 space-y-8 container-text">
      <h1 class="header-1">Colabore</h1>
      <p class="text-lg">A plataforma METAMEMO é aberta e você pode colaborar conosco</p>
      <button
        class="btn"
        onclick="window.location = `/colaborar`"
      >Acesse aqui</button>
    </article>
  </section>
</template>
