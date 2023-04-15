<script setup lang="ts">
import LogoGithub from "@vicons/carbon/LogoGithub";
import { NIcon } from "naive-ui";
import { useMeta } from "vue-meta";
import bgFam from "../assets/imgs/familia-bolsonaro.png";
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
  <section class="bg-gradient-to-r from-cyan-600 to-blue-700 dark:from-cyan-700 dark:to-blue-800">
    <article class="pt-24 pb-32 space-y-8 text-white dark:text-gray-300 px-8 container-text">
      <h1 class="text-3xl sm:text-center font-bold leading-10 dark:text-gray-100">Um metamemo é uma coleção de dados, metadados e mídias agregadas de publicações de um ou mais perfis de redes sociais em um único arquivo.</h1>
    </article>
  </section>
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
  <section class="flex flex-col xl:flex-row">
    <div class="bg-gradient-to-r from-gray-400 to-transparent dark:from-gray-500 lg:min-h-full flex-1 flex items-end justify-center">
      <div class="md:pt-24">
        <img :src="bgFam" alt="Família bolsonaro" />
      </div>
    </div>
    <article class="flex-1 flex items-center">
      <div class="mx-auto px-8 py-32 space-y-12">
        <h1 class="header-1 text-blue-800">Bolsodata, a primeira implementação do MetaMemo.</h1>
        <p class="text-blue-900 font-semibold dark:text-gray-300">O projeto BOLSODATA reuniu as publicações das figuras públicas da Família Bolsonaro (Jair, e seus filhos Flávio, Carlos e Eduardo, respectivamente Presidente, Senador, Vereador e Deputado) de notório interesse público no Brasil quando o projeto começou - em 2021.<br><br>

Para este caso, também foram inseridas informações do contexto brasileiro sobre o período coletado (2010-2022), de forma a possibilitar a identificação um fato isolado publicado pelos perfis em conjunto ao que estava acontecendo no Brasil no mesmo momento através de outros canais midiáticos (mídia impressa, digital e audiovisual). Este levantamento derivou uma reportagem cronológica, em forma de linha do tempo aqui chamada de “Os Bolsonaros” de 1951-2018, que pode ser acessada no link abaixo.
        </p>
      </div>
    </article>
  </section>
  <section class="h-96 flex flex-col justify-center items-center gap-3 text-gray-800 text-white bg-gradient-to-r from-blue-500 to-indigo-500 dark:from-blue-600 dark:to-indigo-800">
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
  </section>
</template>


<style scoped>
.list-title {
  @apply font-bold pb-3 pt-6;
}
.about-page-color {
 @apply text-gray-700 dark:text-gray-300;
}
</style>
