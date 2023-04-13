<script setup lang="ts">
import LogoGithub from "@vicons/carbon/LogoGithub";
import { NIcon } from "naive-ui";
import { useMeta } from "vue-meta";
useMeta({
  title: "Sobre",
  description: "Conheça mais sobre o projeto",
  htmlAttrs: { lang: "pt-br", amp: true },
});
</script>

<template>
  <article class="pt-24 pb-32 space-y-8 container-text about-page-color">
    <h1 class="header-1">O que é a METAMEMO</h1>
    <p class="text-lg">METAMEMO é um sistema criado para coletar, armazenar, processar e visualizar as publicações de qualquer perfil em plataformas de redes sociais da Internet (Facebook, Instagram, Twitter e Youtube).</p>
    <p class="font-bold">O objetivo é preservar a memória e facilitar a análise desse conteúdo por parte de ativistas, jornalistas e pesquisadores.</p>
  </article>
  <div class="bg-gradient-to-r from-cyan-600 to-blue-700 dark:from-cyan-700 dark:to-blue-800">
    <article class="pt-24 pb-32 space-y-8 text-white dark:text-gray-300 px-8 container-text">
      <h1 class="text-3xl sm:text-center font-bold leading-10 dark:text-gray-100">Um metamemo é uma coleção de dados, metadados e mídias agregadas de publicações de um ou mais perfis de redes sociais em um único arquivo.</h1>
    </article>
  </div>
  <article class="pt-24 pb-32 space-y-8 dark:text-gray-300 px-8 container-text about-page-color">
    <h1 class="header-1">METAMEMO funciona em quarto partes</h1>
    <ol class="list-decimal space-y-4 pt-6 text-lg">
      <li>
        <h2 class="list-title">Coletores</h2>
        <p>Um coletor é um script que executa uma tarefa periodicamente em um determinado cronograma. Exemplo: “coletar conteúdo, imagem, data e outras informações de um perfil no Facebook de janeiro de 2011 até dezembro de 2022”. Os dados, aqui chamados de metaitem (em formato texto) são apresentados em cada metamemo, enquanto as imagens (arquivos que exigem mais quantidade de memória) são armazenados em um servidor próprio.</p>
      </li>
      <li>
        <h2 class="list-title">Processadores</h2>
        <p>Um processador é uma ferramenta que, alimentada pelas informações das redes sociais trazidas pelos coletores, limpa e processa os dados, gerando também novos metadados. Exemplo: “transformar todo conteúdo de um perfil de Twitter de 11 de janeiro de 2011 até dezembro de 2022 em uma nuvem de tags, onde quanto maior a tag maior a frequência de sua aparição na coleta.</p>
      </li>
      <li>
        <h2 class="list-title">Armazenagem</h2>
        <p>Após coletados e processados, os metaitens são armazenados em um banco de dados com suporte a full-text search, ou seja: que a busca por palavras possa retornar automaticamente uma ou todas as palavras buscadas, não apenas a palavra exata.</p>
      </li>
      <li>
        <h2 class="list-title">Visualização</h2>
        <p>Depois de coletados, processados e armazenados, os metaitens eles então serão mostrados em uma interface visual acessível e administrável. A busca por um metamemo de uma determinada pessoa, num período delimitado, retorna uma série de postagens, que são separadas por rede social, com a possibilidade de clicar em cada post para ver o texto e a imagem (ou vídeo) na íntegra em outra tela.</p>
      </li>
    </ol>
  </article>
  <div class="h-96 flex flex-col justify-center items-center gap-3 text-gray-800 text-white bg-gradient-to-r from-blue-500 to-indigo-500 dark:from-blue-600 dark:to-indigo-800">
    <div class="flex items-center gap-6">
      <h1 class="text-3xl font-bold">Fork me on Github</h1>
      <div>
        <button
          type="button"
          class="btn btn-icon"
          onclick="window.open(`https://github.com/funesomemorioso/metamemo`);"
          title="Acessar repositório de projeto"
        >
          <n-icon :component="LogoGithub" />
        </button>
      </div>
    </div>
  </div>
</template>


<style scoped>
.container-text {
  @apply container mx-auto px-8 2xl:px-32 lg:max-w-5xl;
}
.header-1 {
  @apply text-5xl font-bold leading-none dark:text-gray-100;
}
.list-title {
  @apply font-bold pb-3 pt-6;
}
.about-page-color {
 @apply text-blue-800 dark:text-gray-300;
}
</style>
