<script lang="ts">
import { ref } from "vue"
import { RouterLink } from "vue-router";

export default {
  props: {
    menuOptions: {
      type: Object,
    }
  },
  setup() {
    const showMobileMenu = ref(false);

    const handlerClick = () => {
      showMobileMenu.value = !showMobileMenu.value
    }

    return {
      showMobileMenu,
      handlerClick
    }
  }
}
</script>
<template>
  <nav class="flex items-center justify-between px-6 py-4 lg:px-8 bg-white dark:bg-black" aria-label="Global">
    <div class="flex lg:flex-1">
      <a href="#" class="-m-1.5 p-1.5">
        <span class="sr-only">Your Company</span>
        <img  class="h-9" src="../assets/mm.svg">
      </a>
    </div>
    <div class="flex lg:hidden">
      <button
        type="button"
        class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700 dark:text-gray-400"
        :onClick="handlerClick"
      >
        <span class="sr-only">Abrir menu principal</span>
        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
        </svg>
      </button>
    </div>
    <div class="items hidden lg:flex lg:gap-x-12">
      <router-link v-for="menu in menuOptions" :to="menu.to.path" class="menu-item">
        {{ menu.label }}
      </router-link>
    </div>
    <div class="hidden lg:flex lg:flex-1 lg:justify-end">
      <slot />
    </div>
  </nav>

  <!-- Mobile menu, show/hide based on menu open state. -->
  <div role="dialog" aria-modal="true">
    <div v-if="showMobileMenu" class="fixed inset-0 z-10 overflow-y-auto bg-white px-6 py-6 lg:hidden bg-white dark:bg-black">
      <div class="flex items-center justify-between">
        <a href="#" class="-m-1.5 p-1.5">
          <span class="sr-only">Your Company</span>
          <img  class="h-9" src="../assets/mm.svg">
        </a>
        <button
          type="button"
          class="-m-2.5 rounded-md p-2.5 text-gray-700 dark:text-gray-300"
          :onClick="handlerClick"
        >
          <span class="sr-only">Close menu</span> 
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="mt-6 flow-root">
        <div class="-my-6 divide-y divide-gray-500/10">
          <div class="items space-y-2 py-6">

            <router-link
              v-for="menu in menuOptions"
              :to="menu.to.path"
              :onClick="handlerClick"
              class="-mx-3 block rounded-lg py-2 px-3 text-base font-semibold leading-7 text-gray-900 dark:text-gray-200 hover:bg-gray-400/10"
            >
              {{ menu.label }}
            </router-link>
            <slot />
          </div>
        </div>
      </div>
    </div>
  </div>

</template>
<style>
.items .router-link-active {
  @apply text-primary dark:text-primary-dark;
}
.menu-item {
  @apply text-sm font-semibold leading-6 text-gray-900 dark:text-gray-200
}
</style>
