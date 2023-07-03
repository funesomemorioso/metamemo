<script setup lang="ts">
const baseUrl = import.meta.env.VITE_API_URL;
</script>

<template>
  <footer aria-label="Site Footer" class="bg-slate-100 dark:bg-zinc-900">
    <div
      class="max-w-screen-xl px-4 py-16 mx-auto space-y-8 sm:px-6 lg:space-y-16 lg:px-8"
    >
      <div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
        <div>
          <img src="../assets/logo.svg" width="70px" />
          <div class="text-gray-800 dark:text-gray-100 text-2xl">
            META<span class="font-bold">memo</span>
          </div>
          <a href="mailto:metamemo@metamemo.info" class="text-xs text-blue-600 dark:text-blue-500">metamemo@metamemo.info</a>

          <p class="max-w-xs mt-4 text-gray-500 dark:text-gray-400">
            Conteúdo original do site licenciado sob <br>
            <a href="https://creativecommons.org/licenses/by-sa/3.0/deed.pt"><b>CC BY SA.</b></a>
          </p>
        </div>

        <div
          class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:col-span-2 lg:grid-cols-4"
        >
          <div class="lg:col-start-2">
            <p class="font-medium text-gray-900 dark:text-white">
              Baixe ou distribua
            </p>

            <nav aria-label="Footer Navigation - Company" class="mt-6">
              <ul class="space-y-4 text-sm">
                <li>
                  <a
                    :href="baseUrl + '/memoitems/download'"
                    class="text-gray-700 transition hover:opacity-75 dark:text-gray-200"
                  >
                    Baixar aqui
                  </a>
                </li>
              </ul>
            </nav>
          </div>

          <div>
            <p class="font-medium text-gray-900 dark:text-white">Colabore</p>

            <nav aria-label="Footer Navigation - Legal" class="mt-6">
              <ul class="space-y-4 text-sm">
                <li>
                  <a
                    href="/collaborate"
                    class="text-gray-700 transition hover:opacity-75 dark:text-gray-200"
                  >
                    Colaborar
                  </a>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>

      <p class="text-xs text-gray-500 dark:text-gray-400">
        2023 <span class="font-bold">Metamemo</span>.
      </p>
    </div>
  </footer>
</template>
