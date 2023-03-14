<script setup lang="ts">
import { useMeta } from "vue-meta"
useMeta({
  title: '',
  description: 'Tela home do projeto metamemo',
  htmlAttrs: { lang: 'pt-br', amp: true }
})
</script>

<template>
  <section class="dark:text-gray-400 dark:bg-black body-font">
    <div class="container px-5 py-40 mx-auto flex flex-wrap items-center">
      <div class="lg:w-3/5 md:w-1/2 md:pr-16 lg:pr-0 pr-0">
        <h1 class="title-font font-medium text-3xl text-gray-800 dark:text-white"><span class="font-bold">METAMEMO</span> é um sistema criado para coletar, armazenar e visualizar as memórias de qualquer pessoa (ou organização, coletivo, empresa, marca).</h1>
      </div>
      <div class="lg:w-2/6 md:w-1/2 bg-gray-100 dark:bg-gray-800 dark:bg-opacity-50 rounded-lg p-8 flex flex-col md:ml-auto w-full mt-10 md:mt-0">
        <h2 class="dark:text-white text-lg font-medium title-font mb-5">Busque um <span class="font-bold">METAMEMO</span></h2>
        <div class="relative mb-4">
          <label for="full-name" class="leading-7 text-sm dark:text-gray-400">Pesquisa</label>
          <input type="text" id="full-name" name="full-name" class="w-full dark:bg-gray-600 bg-opacity-20 focus:bg-transparent focus:ring-2 focus:ring-indigo-900 rounded border dark:border-gray-600 focus:border-indigo-500 text-base outline-none dark:text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out">
        </div>
        <div class="relative mb-4">
          <label for="email" class="leading-7 text-sm dark:text-gray-400">Campo</label>
          <input type="email" id="email" name="email" class="w-full dark:bg-gray-600 bg-opacity-20 focus:bg-transparent focus:ring-2 focus:ring-indigo-900 rounded border dark:border-gray-600 focus:border-indigo-500 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out">
        </div>
        <button class="text-white bg-primary border-0 py-2 px-8 focus:outline-none hover:bg-primary-dark rounded text-lg">Consultar</button>
        <p class="text-xs mt-3">Clique e efetue uma consulta em nossa base de dados.</p>
      </div>
    </div>
  </section>
</template>
