<script setup lang="ts">
import Article from "../components/Article.vue"
import { useMeta } from "vue-meta"
useMeta({
  title: 'Colaborar',
  description: 'Colabore com o nosso projeto',
  htmlAttrs: { lang: 'pt-br', amp: true }
})
</script>
<template>
  <Article title="Colaborar" />
</template>
<style>
</style>
