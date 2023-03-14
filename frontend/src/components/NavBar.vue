<script lang="ts">
import { ref, watch, onBeforeMount } from "vue"
import { RouterLink } from "vue-router";
import { useRoute } from "vue-router";

export default {
  props: {
    menuOptions: {
      type: Object,
    },
    menuActive: {
      type: String,
    }
  },
  setup() {
    const showMobileMenu = ref(false);
    const route = useRoute();
    const active = ref({});

    const handlerClick = () => {
      showMobileMenu.value = !showMobileMenu.value
    }

    const menuActive = () => {
      if ((route.path.split("/").length - 1) == 1) {
        route.path.substring(1)
      }
      const regex = /\//g
      return route.path.replace(regex, ' ').trim().split(' ')[0]
    }

    onBeforeMount(()=>{
      active.value = menuActive()
    })

    watch(() => route.path, () => {
        active.value = menuActive()
    })

    return {
      showMobileMenu,
      handlerClick,
      active 
    }
  }
}
</script>
<template>
  <div class="bg-slate-100 dark:bg-gray-900"> 
    <nav class="flex items-center justify-between py-4 container-default" aria-label="Global">
      <div class="flex lg:flex-1">
        <div class="-m-1.5 p-1.5">
          <router-link
              :to="'/'"
              class="flex items-center gap-3 hover:outline outline-offset-8 outline-2  outline-gray-500 rounded"
              >
              <img class="h-9" src="../assets/logo.svg">
              <div class="text-gray-800 dark:text-gray-100 font-base">
                META<span class="font-bold">memo</span>
              </div>
          </router-link>
        </div>
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
        <router-link v-for="menu in menuOptions" :to="menu.to.path" class="menu-item" :class="active == menu.to.name ? 'active' : ''" >
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
        <div class="flex justify-between">
          <div class="flex items-center gap-2">
            <img class="h-9" src="../assets/logo.svg">
            <div class="text-gray-800 dark:text-gray-100 font-base">
              META<span class="font-bold">memo</span>
            </div>
          </div>
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
                  class="-mx-3 block rounded-lg py-2 px-3 text-base leading-7 text-gray-900 dark:text-gray-200 hover:bg-gray-400/10"
                  >
                  {{ menu.label }}
              </router-link>
                <slot />
            </div>
          </div>
        </div>
      </div> 
    </div>
  </div>
</template>
<style>
.items .active {
  @apply text-primary dark:text-primary ;
}
.menu-item {
  @apply hover:text-primary-dark hover:dark:text-primary;
}
.menu-item {
  @apply text-sm font-semibold leading-6 text-gray-900 dark:text-gray-200
}
</style>
