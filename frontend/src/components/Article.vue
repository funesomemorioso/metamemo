<script lang="ts">
export default {
    props: ['title'],
    setup(props) {
        return {
            title: props.title
        }
    }
}
</script>
<template>
  <article class="max-w-4xl mx-auto space-y-16 padding-y-default">
    <div class="w-full mx-auto space-y-4">
      <h1 class="text-5xl font-bold leading-none">{{ title }} et malesuada fames ac ante ipsum primis in faucibus?</h1>
      <div class="flex flex-wrap space-x-2 text-sm dark:text-gray-300">
        <a rel="noopener noreferrer" href="#" class="p-1 hover:underline">#Test</a>
        <a rel="noopener noreferrer" href="#" class="p-1 hover:underline">#TailwindCSS</a>
      </div>
      <p class="text-sm dark:text-gray-300">by
      <a href="#" target="_blank" rel="noopener noreferrer" class="hover:underline dark:text-primary">
        <span>Leroy Jenkins</span>
      </a>on
      <time datetime="2021-02-12 15:34:18-0200">Feb 12th 2021</time>
      </p>
    </div>
    <div class="dark:text-gray-300">
      <p>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque, sapiente incidunt. Rem at magni, dicta doloribus ratione labore exercitationem eius, fugit possimus saepe delectus iure alias id recusandae hic placeat.
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque, sapiente incidunt. Rem at magni, dicta doloribus ratione labore exercitationem eius, fugit possimus saepe delectus iure alias id recusandae hic placeat.
      </p>
    </div>
  </article>
</template>
<style></style>
