<script setup lang="ts">
</script>

<template>
  <section class="body-font self-center padding-y-default">
    <div class="container mx-auto flex md:flex-row flex-col items-center">
      <div class="lg:flex-grow md:w-1/2 lg:pr-24 md:pr-16 flex flex-col md:items-start md:text-left mb-16 md:mb-0 items-center text-center">
        <h1 class="title-font sm:text-4xl text-3xl mb-4 font-medium">Metamemo</h1>
        <p class="mb-6 leading-relaxed">Execute uma pesquisa em nossa base de dados.</p>
        <div class="flex w-full md:justify-start justify-center items-end">
          <router-link
              :to="'consulta/lista'"
          >
              <button 
                class="inline-flex text-white bg-indigo-500 border-0 py-2 px-6 focus:outline-none hover:bg-indigo-600 rounded text-lg"
              >
              Consultar
              </button>
          </router-link>
        </div>
      </div>
      <div class="lg:max-w-lg lg:w-full md:w-1/2 w-5/6">
        <img class="object-cover object-center rounded" alt="hero" src="https://dummyimage.com/720x600">
      </div>
    </div>
  </section>
</template>
