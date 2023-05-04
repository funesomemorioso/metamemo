<script lang="ts">
import { defineComponent, watch, ref } from "vue";
import { useStore } from "vuex";
import { NModal, NCarousel, NImage } from "naive-ui";
import type { Ref } from "vue";

export default defineComponent({
  components: { NModal, NCarousel, NImage },
  setup() {
    const store = useStore();
    const showModal = ref(false);
    const content: Ref<{ media_urls: Array<string> }> = ref({ media_urls: [] });
    const text = ref("");
    const dateTime = ref(null);
    const endsWithAny = (str: string, suffixes: Array<string>) => {
      return suffixes.some((suffix) => str.endsWith(suffix));
    };
    const handleCloseButton = () => {
      const imgPreview = document.querySelector(".n-image-preview-container");
      // If imgPreview active don`t close modal
      if (imgPreview) {
        return;
      }
      store.commit("SHOW_POST_MODAL", false);
    };
    watch(
      () => [store.state.modalPost.showModal],
      () => {
        showModal.value = store.state.modalPost.showModal;
        content.value = store.state.modalPost.content;
        text.value = store.state.modalPost.text;
        dateTime.value = store.state.modalPost.dateTime;
      }
    );
    return {
      showModal,
      dateTime,
      content,
      text,
      endsWithAny,
      bodyStyle: {
        width: "600px",
      },
      handleCloseButton,
    };
  },
});
</script>

<template>
  <n-modal
    v-model:show="showModal"
    class="custom-card"
    preset="card"
    title="Postagem"
    :style="bodyStyle"
    :bordered="false"
    size="huge"
    @close="handleCloseButton"
  >
    <template #header-extra>
      <section class="header-content">
        <span>
          {{ dateTime }}
        </span>
      </section>
    </template>
    <div class="mb-6">
      {{ text }}
    </div>
    <div
      v-if="content.media_urls && content.media_urls.length"
      class="pt-8 flex gap-2 h-96"
    >
      <n-carousel
        :dot-placement="'top'"
        :loop="false"
        :show-arrow="content.media_urls.length > 1 ? true : false"
        class="bg-gray-500 dark:bg-zinc-700 rounded"
        draggable
      >
        <template v-for="(el, index) in content.media_urls" :key="index">
          <video v-if="endsWithAny(el, ['mp4', 'mpeg', 'mkv'])" controls>
            <source :src="el" />
          </video>
          <n-image
            v-else
            :src="el"
            :fallback-src="'https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg'"
          />
        </template>
      </n-carousel>
    </div>
  </n-modal>
</template>
<style>
.n-image-preview-toolbar {
  @apply flex gap-5;
}

.n-carousel__slide {
  @apply flex justify-center;
}

.n-image img {
 object-fit: contain !important;
}
</style>

<style scoped>
.n-image {
  @apply justify-center;
}

.header-content {
  @apply flex justify-end gap-2;
}

.social-numbers {
  @apply flex justify-end gap-2;
}

.number-element {
  @apply flex gap-2 items-center border border-gray-500 px-4 py-1 rounded-2xl;
}
</style>
