<script setup lang="ts">
import LogoGithub from "@vicons/carbon/LogoGithub";
import { NIcon } from "naive-ui";
import { useMeta } from "vue-meta";
useMeta({
  title: "Colaborar",
  description: "Colabore com o nosso projeto",
  htmlAttrs: { lang: "pt-br", amp: true },
});

const downloadLink = () =>
  (window.location.href = (import.meta.env.VITE_API_URL + "/memoitems/download"));
</script>
<template>
  <div
    class="flex flex-col gap-24 xl:flex-row container mx-auto md:px-8 2xl:px-32"
  >
    <div class="text-white">
      <article class="flex flex-col mx-auto space-y-8 pt-64 pb-32 px-8">
        <h1 class="text-4xl font-medium">
          Baixe, armazene e/ou distribua via torrent este <span class="font-bold">metamemo</span>.
        </h1>
        <div>
          <button type="button" class="btn" @click="downloadLink">Baixe aqui</button>
        </div>
      </article>
    </div>
    <div
      class="xl:max-w-2xl bg-white dark:bg-gray-800 sm:rounded-2xl mt-5 sm:mb-5 bg-clip-padding bg-opacity-80 dark:bg-opacity-80 backdrop-filter"
    >
      <article class="mx-auto py-20 px-0 px-8 sm:px-16 space-y-4">
        <h1 class="text-3xl font-bold">
          Remixe esta base de dados para novas implementações, desenvolvimentos, derivações e usos do metamemo BolsoData.
        </h1>
        <h2 class="text-xl">Conteúdo original do site licenciado sob <a class="text-blue-500 font-medium" href="https://creativecommons.org/licenses/by-sa/3.0/deed.pt">CC BY SA.</a></h2>
        <p class="text-xl font-bold">Você pode:</p>
        <ul class="list-disc font-medium text-lg space-y-2 px-6">
          <li><strong>Compartilhar:</strong> copiar e redistribuir o material em qualquer suporte ou formato;</li>
          <li><strong>Adaptar:</strong> remixar, transformar, e criar a partir do material para qualquer fim, mesmo que comercial;</li>
          <li><strong>Você deve</strong> dar o crédito apropriado, prover um link para a licença e indicar se mudanças foram feitas;</li>
          <li><strong>Compartilha Igual:</strong> Se você remixar, transformar, ou criar a partir do material, tem de distribuir as suas contribuições sob a mesma licença que o original.</li>
        </ul>
      </article>
    </div>
  </div>
  <div class="bg-white dark:bg-gray-800 bg-clip-padding bg-opacity-80 dark:bg-opacity-80 backdrop-filter h-64 flex flex-col justify-center items-center gap-3 dark:text-white">
    <div class="flex items-center gap-4">
      <h1 class="text-2xl font-bold">Por gentileza remixar</h1>
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
    <a
      class="text-xl hover:opacity-50"
      title="Enviar email"
      href="mailto:metamemo@metamemo.info"
    >
      metamemo@metamemo.info
    </a>
  </div>
</template>

<style></style>
