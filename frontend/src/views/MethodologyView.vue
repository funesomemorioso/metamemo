<script setup lang="ts">
import Article from "../components/Article.vue";
import { useMeta } from "vue-meta";
useMeta({
  title: "Metodologia",
  description: "Conheça a metodologia aplicada no projeto",
  htmlAttrs: { lang: "pt-br", amp: true },
});
</script>
<template>
  <article class="pt-20 pb-32 space-y-8 container-text about-page-color">
    <div class="text-center text-gray-800 dark:text-gray-200">
      <h1 class="text-5xl">METODOLOGIA</h1>
      <h2 class="text-3xl font-bold">METAMEMO</h2>
    </div>
    <div class="grid grid-cols-12 gap-y-10 md:gap-x-10 pt-12">
      <div class="methodology-content row-span-2">
        <h2 class="methodology-content-title">O QUE É</h2>
        <div class="methodology-content-text">
          <p>METAMEMO é um sistema criado para coletar, armazenar, processar e visualizar as memórias de um perfil nas principais plataformas de redes sociais da internet. O objetivo é preservar e facilitar a análise desse conteúdo por parte de ativistas, jornalistas e pesquisadores.
          </p>
          <p>
          Um metamemo é uma coleção de dados, metadados e mídias agregadas de publicações de um ou mais perfis de redes sociais em um único arquivo.
          </p>
        </div>
      </div>
      <div class="methodology-content">
        <h2 class="methodology-content-title">PROCESSADORES</h2>
        <div class="methodology-content-text">
          <p>Um processador é uma ferramenta que, alimentada pelas informações das redes sociais trazidas pelos coletores, limpa e processa os dados, gerando também novos metadados.
          </p>
        </div>
      </div>
      <div class="methodology-content row-span-4">
        <h2 class="methodology-content-title">ARMAZENAGEM</h2>
        <div class="methodology-content-text">
          <p>Depois dos dados serem coletados, processados e armazenados, eles então serão mostrados em uma interface visual acessível. Uma busca por um metamemo de uma determinada pessoa, num período delimitado, retorna uma série de postagens, que são visualizadas divididas por rede social, com a possibilidade de clicar em cada post para ver o texto e a imagem (ou vídeo) na íntegra em outra tela.</p>
          <p>A primeira implementação da MetaMemo foi o projeto chamado BOLSODATA, que inclui a Família Bolsonaro (Jair, o pai, e seus filhos Flávio, Carlos e Eduardo), todos figuras públicas (Presidente, Senador, Vereador e Deputado) de notório interesse público no Brasil quando o projeto começou (2021). A proposta foi então organizar a coleta, processamento, armazenamento e visualização dos dados das redes sociais dessas quatro pessoas.</p>
          <p>Para este caso, também foi preparado material extra:</p>
          <ul class="list-disc space-y-4 text-sm">
            <li>Informações do contexto brasileiro sobre o período coletado (2010-2022), de forma a facilitar o entendimento de um fato isolado vivenciado ou comentado pelos citados com o que estava acontecendo no Brasil no mesmo momento.</li>
            <li>Uma reportagem cronológica sobre os Bolsonaros a partir de pesquisa em arquivos (mídia impressa, digital e audiovisual) em forma de Linha do Tempo - Os Bolsonaros 1951-2018;</li>
            <li>Coletor de notícias de veículos de mídia (Folha de S.Paulo, G1 e Estadão);</li>
            <li>Reprodução da capa de jornais (Folha de S. Paulo)</li>
          </ul>

        </div>
      </div>
      <div class="methodology-content">
        <h2 class="methodology-content-title">COMO FUNCIONA?</h2>
        <div class="methodology-content-text">
          <p>O sistema é dividido em quatro partes: coletores, processadores, armazenagem e visualização.</p>
        </div>
      </div>
      <div class="methodology-content">
        <h2 class="methodology-content-title">COLETORES</h2>
        <div class="methodology-content-text">
          <p>
          Um coletor é um script que executa uma tarefa periodicamente em um determinado cronograma, como por exemplo: “coletar conteúdo, imagem, data e outras informações de um perfil no Facebook de janeiro de 2011 até dezembro de 2022”.
          </p>
          <p><strong>FACEBOOK - TWITTER - YOUTUBE - INSTAGRAM - TELEGRAM - BLOGSPOT</strong></p>
          <p>
          Os dados (em formato texto) são apresentados em cada metamemo, enquanto as imagens (arquivos que exigem mais memória) são armazenados em um servidor próprio.
          </p>
        </div>
      </div>
    </div>
  </article>
  <section class="bg-gradient-to-r from-cyan-600 to-blue-700 dark:from-cyan-700 dark:to-blue-800">
    <article class="pt-24 pb-32 space-y-8 text-white dark:text-gray-300 px-8 container-text">
    <div class="grid grid-cols-12 gap-y-10 md:gap-x-12">
      <div class="methodology-content">
        <h2 class="text-3xl font-bold text-white">HISTÓRIA</h2>
        <div class="text-white text-base">
          <p>O projeto começou em outubro de 2021 com a organização de duas frentes de trabalho: desenvolvimento, responsável por buscar soluções técnicas para coletar, armazenar e processar os dados; e pesquisa, responsável pela organização dos materiais coletados, pesquisa de conteúdo relacionados, entrevistas com pesquisadores e jornalistas que fazem ou fizeram trabalho semelhante e concepção da visualização final dos dados (a plataforma) - esta parte logo depois desmembrada em design, em comunicação direta também com o desenvolvimento. No mês seguinte, a frente de parcerias surgiu para organizar formas de trabalhar com as coleções de memórias da MetaMemo em colaboração com outras organizações, pessoas, grupos e coletivos, seja a partir de parcerias diretas ou no estímulo a pesquisadores e projetos que possam utilizar os dados das MetaMemos.</p>
        </div>
      </div>
      <div class="methodology-content">
        <h2 class="text-3xl font-bold text-white">PESQUISA</h2>
        <div class="text-white text-base">
          <p>A pesquisa conceitual para o projeto foi realizada a partir de uma investigação exploratória, com entrevistas semi-estruturadas com cerca de 10 pesquisadores e jornalistas que trabalham com materiais de arquivo digital e/ou pesquisam temáticas ligadas à políticas e tecnologias. O objetivo foi buscar mais informações sobre como pesquisadores e jornalistas fazem suas investigações com fontes digitais, quais as dificuldades de pesquisa ligadas às redes sociais, os desafios da pesquisa sobre temas de política brasileira na internet, os cuidados necessários para a segurança e o anonimato quando os tópicos podem trazer riscos aos investigadores; as formas de extrair, processar e armazenar massa de dados; ferramentas mais utilizadas; compartilhamento de bases de dados dos mesmos tópicos do projeto; entre outros temas. As entrevistas não foram divulgadas externamente. </p>
        </div>
      </div>
    </div>
    </article>
  </section>
  <article class="pt-24 pb-32 space-y-8 dark:text-gray-300 px-8 container-text about-page-color">
    <h1 class="header-1 text-center pb-6">BOLSODATA</h1>
    <p class="text-base">
    A primeira implementação da MetaMemo foi o projeto chamado BOLSODATA, que reuniu as postagens da Família Bolsonaro (Jair e seus filhos Flávio, Carlos e Eduardo), todos figuras públicas (Presidente, Senador, Vereador e Deputado) de notório interesse público no Brasil quando o projeto começou (2021).<br><br>

    A proposta foi então organizar a coleta, processamento, armazenamento e visualização dos dados das redes sociais dessas quatro pessoas. Para este caso, também foram inseridas informações sobre fatos de interesse público ocorridos no Brasil no período coletado (2010-2021), de forma a contextualizar as informações postadas nas redes sociais; e uma reportagem cronológica, em formato de linha do tempo, chamada “Os Bolsonaros - 1951-2018, com informações coletadas em livros, veículos jornalísticos (mídia impressa, digital e audiovisual), acervo da Câmara dos Deputados, entre outras fontes.<br><br>

A escolha deste case específico ajuda a ilustrar como pode funcionar a MetaMemo demonstra as funcionalidades e formas de visualização da plataforma como também para a equipe desenvolvedora testar soluções para uma efetiva realização das etapas de coleta, processamento e armazenamento dos dados.
    </p>
    <h2 class="font-bold">ETAPA 1: OUTUBRO / NOVEMBRO / DEZEMBRO DE 2021</h2>
    <ul class="list-disc space-y-2">
      <li>Testes com raspadores de dados de redes sociais já existentes, seja em plataformas proprietárias (como CrowdTangle) como em outros com código disponibilizados no Github ou GitLab;</li>
      <li>Primeiras raspagens dos dados das redes dos Bolsonaros, processamento do material bruto coletado de forma a facilitar a visualização;</li>
      <li>Entrevistas de contexto com pesquisadores e pessoas que estão coletando informações adjacentes;</li>
      <li>“Raspagem manual” de matérias na mídia sobre Bolsonaros (2010-2021) para pesquisa para reportagem - Linha do tempo e sobre fatos ocorridos no Brasil no período;</li>
      <li>Produção da linha do tempo Brasil, com fatos relevantes no país de 2010 até 2021;</li>
      <li>Checagem e seleção dos campos para serem apresentados na plataforma: após a raspagem, “pente fino” nas informações para selecionar o que precisa ser visualizado na plataforma final e o que pode ser descartado (ou deixado de pano de fundo);</li>
    </ul>
    <h2 class="font-bold">ETAPA 2: JANEIRO, FEVEREIRO E MARÇO DE 2022</h2>
    <ul class="list-disc space-y-2">
      <li>Testes com raspadores de dados de redes sociais já existentes, seja em plataformas proprietárias (como CrowdTangle) como em outros com código disponibilizados no Github ou GitLab;</li>
      <li>Primeiras raspagens dos dados das redes dos Bolsonaros, processamento do material bruto coletado de forma a facilitar a visualização;</li>
      <li>Entrevistas de contexto com pesquisadores e pessoas que estão coletando informações adjacentes;</li>
      <li>“Raspagem manual” de matérias na mídia sobre Bolsonaros (2010-2021) para pesquisa para reportagem - Linha do tempo e sobre fatos ocorridos no Brasil no período;</li>
      <li>Produção da linha do tempo Brasil, com fatos relevantes no país de 2010 até 2021;</li>
      <li>Checagem e seleção dos campos para serem apresentados na plataforma: após a raspagem, “pente fino” nas informações para selecionar o que precisa ser visualizado na plataforma final e o que pode ser descartado (ou deixado de pano de fundo);</li>
    </ul>
  </article>
</template>

<style scoped>
.container-text {
  @apply container mx-auto px-8 2xl:px-32 lg:max-w-5xl;
}
.methodology-content {
  @apply col-span-12 md:col-span-6 space-y-5;
}
.methodology-content-title {
  @apply text-base font-semibold text-gray-700 dark:text-gray-100;
}
.methodology-content-text {
  @apply text-base space-y-4 text-gray-600 dark:text-gray-300;
}
</style>

