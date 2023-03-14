<script setup lang="ts">
import Article from "../components/Article.vue"
import { useMeta } from "vue-meta"
useMeta({
  title: 'Sobre',
  description: 'Conheça mais sobre o projeto',
  htmlAttrs: { lang: 'pt-br', amp: true }
})
</script>
<template>
  <Article title="Sobre" />
</template>
<style>
</style>
