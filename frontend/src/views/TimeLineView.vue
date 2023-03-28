<script setup lang="ts">
import { useMeta } from "vue-meta";
import { NAnchor, NAnchorLink } from "naive-ui";
import { onMounted, onBeforeUnmount } from "vue";

useMeta({
  title: "Linha do tempo",
  description: "Linha do tempo dos dados catalogados",
  htmlAttrs: { lang: "pt-br", amp: true },
});

onMounted(() => {
  document.querySelector("html")?.classList.add("scroll-smooth");
});

onBeforeUnmount(() => {
  document.querySelector("html")?.classList.remove("scroll-smooth");
});
</script>

<template>
  <section class="dark:text-gray-200 pt-12 pb-32">
    <div class="container px-4 py-12 grid grid-cols-12">
      <div class="grid gap-4 sm:grid-cols-6 sm:col-span-9">
        <div class="col-span-12 sm:col-span-3">
          <div class="text-center sm:text-left mb-14">
            <h3 id="basic.vue" class="text-3xl font-semibold">Morbi tempor</h3>
            <span
              class="text-sm font-bold tracking-wider uppercase dark:text-gray-500"
              >Vestibulum diam nunc</span
            >
          </div>
        </div>
        <div class="relative col-span-12 px-4 space-y-6 sm:col-span-9">
          <div
            class="col-span-12 space-y-12 relative px-4 flex flex-col gap-20 sm:col-span-8 sm:space-y-8 sm:before:absolute sm:before:top-2 sm:before:bottom-0 sm:before:w-0.5 sm:before:-left-3 before:bg-gradient-to-b before:from-gray-400"
          >
            <div
              class="flex flex-col sm:relative sm:before:absolute sm:before:top-2 sm:before:w-4 sm:before:h-4 sm:before:rounded-full sm:before:left-[-35px] sm:before:z-[1] before:dark:bg-violet-600 before:bg-primary"
            >
              <h3
                id="ignore-gap.vue"
                class="text-xl font-semibold tracking-wide"
              >
                Donec porta enim vel
              </h3>
              <time class="text-xs tracking-wide uppercase dark:text-gray-400"
                >Dec 2020</time
              >
              <p class="mt-3">
                Pellentesque feugiat ante at nisl efficitur, in mollis orci
                scelerisque. Interdum et malesuada fames ac ante ipsum primis in
                faucibus.
              </p>
            </div>
            <div
              class="flex flex-col sm:relative sm:before:absolute sm:before:top-2 sm:before:w-4 sm:before:h-4 sm:before:rounded-full sm:before:left-[-35px] sm:before:z-[1] before:dark:bg-violet-600 before:bg-primary"
            >
              <h3 class="text-xl font-semibold tracking-wide">
                Aliquam sit amet nunc ut
              </h3>
              <time class="text-xs tracking-wide uppercase dark:text-gray-400"
                >Jul 2019</time
              >
              <p class="mt-3">
                Morbi vulputate aliquam libero non dictum. Aliquam sit amet nunc
                ut diam aliquet tincidunt nec nec dui. Donec mollis turpis eget
                egestas sodales.
              </p>
            </div>
            <div
              class="flex flex-col sm:relative sm:before:absolute sm:before:top-2 sm:before:w-4 sm:before:h-4 sm:before:rounded-full sm:before:left-[-35px] sm:before:z-[1] before:dark:bg-violet-600 before:bg-primary"
            >
              <h3 class="text-xl font-semibold tracking-wide">
                Pellentesque habitant morbi
              </h3>
              <time class="text-xs tracking-wide uppercase dark:text-gray-400"
                >Jan 2016</time
              >
              <p class="mt-3">
                Suspendisse tincidunt, arcu nec faucibus efficitur, justo velit
                consectetur nisl, sit amet condimentum lacus orci nec purus.
                Mauris quis quam suscipit, vehicula felis id, vehicula enim.
              </p>
            </div>
            <div
              class="flex flex-col sm:relative sm:before:absolute sm:before:top-2 sm:before:w-4 sm:before:h-4 sm:before:rounded-full sm:before:left-[-35px] sm:before:z-[1] before:dark:bg-violet-600 before:bg-primary"
            >
              <h3 class="text-xl font-semibold tracking-wide">
                Pellentesque habitant morbi
              </h3>
              <time class="text-xs tracking-wide uppercase dark:text-gray-400"
                >Jan 2016</time
              >
              <p class="mt-3">
                Suspendisse tincidunt, arcu nec faucibus efficitur, justo velit
                consectetur nisl, sit amet condimentum lacus orci nec purus.
                Mauris quis quam suscipit, vehicula felis id, vehicula enim.
              </p>
            </div>
            <div
              class="flex flex-col sm:relative sm:before:absolute sm:before:top-2 sm:before:w-4 sm:before:h-4 sm:before:rounded-full sm:before:left-[-35px] sm:before:z-[1] before:dark:bg-violet-600 before:bg-primary"
            >
              <h3 class="text-xl font-semibold tracking-wide">
                Pellentesque habitant morbi
              </h3>
              <time class="text-xs tracking-wide uppercase dark:text-gray-400"
                >Jan 2016</time
              >
              <p class="mt-3">
                Suspendisse tincidunt, arcu nec faucibus efficitur, justo velit
                consectetur nisl, sit amet condimentum lacus orci nec purus.
                Mauris quis quam suscipit, vehicula felis id, vehicula enim.
              </p>
            </div>
            <div
              class="flex flex-col sm:relative sm:before:absolute sm:before:top-2 sm:before:w-4 sm:before:h-4 sm:before:rounded-full sm:before:left-[-35px] sm:before:z-[1] before:dark:bg-violet-600 before:bg-primary"
            >
              <h3 class="text-xl font-semibold tracking-wide">
                Pellentesque habitant morbi
              </h3>
              <time class="text-xs tracking-wide uppercase dark:text-gray-400"
                >Jan 2016</time
              >
              <p class="mt-3">
                Suspendisse tincidunt, arcu nec faucibus efficitur, justo velit
                consectetur nisl, sit amet condimentum lacus orci nec purus.
                Mauris quis quam suscipit, vehicula felis id, vehicula enim.
              </p>
            </div>
          </div>
        </div>
      </div>
      <div style="width: 192px" class="sm:col-span-3 relative">
        <n-anchor
          class="anchor"
          :bound="200"
          :show-background="true"
          type="block"
        >
          <n-anchor-link title="Basic" href="#basic.vue" />
          <n-anchor-link title="Ignore-Gap" href="#ignore-gap.vue" />
          <n-anchor-link title="Affix" href="#affix.vue" />
          <n-anchor-link title="Scroll To" href="#scrollto.vue" />
          <n-anchor-link title="API" href="#API" />
        </n-anchor>
      </div>
    </div>
  </section>
</template>

<style scoped>
.n-anchor {
  @apply sticky top-16 z-20;
}
</style>
