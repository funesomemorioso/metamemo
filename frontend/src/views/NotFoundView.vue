<script lang="ts">
import { useMeta } from "vue-meta";
import { NResult, NButton } from "naive-ui";
import { useRouter } from "vue-router";

export default {
  components: { NResult, NButton },
  setup() {
    useMeta({
      title: "404 Não Encontrado",
      description: "Não encontrado",
      htmlAttrs: { lang: "pt-br", amp: true },
    });

    const router = useRouter();
    const goHome = () => {
      router.push("/");
    };

    return { goHome };
  },
};
</script>

<template>
  <n-result
    class="py-44"
    status="error"
    title="404 Não encontrado"
    description="Nenhuma página encontrada para esse endereço."
  >
    <template #footer>
      <n-button :onClick="goHome">Ir para Home</n-button>
    </template>
  </n-result>
</template>

