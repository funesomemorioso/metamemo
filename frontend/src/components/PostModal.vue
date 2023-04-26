<script lang="ts">
import { defineComponent, watch, ref } from "vue";
import { useStore } from "vuex";
import { NModal, NCarousel } from "naive-ui";
import type { Ref } from "vue";

export default defineComponent({
  components: { NModal, NCarousel },
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
    <n-carousel
      :dot-placement="'top'"
      :loop="false"
      :show-arrow="content.media_urls.length > 1 ? true : false"
      class="carousel-img"
      draggable
    >
      <div v-for="(el, index) in content.media_urls" :key="index">
        <video v-if="endsWithAny(el, ['mp4', 'mpeg', 'mkv'])" controls>
          <source :src="el" />
        </video>
        <img v-else :src="el" />
      </div>
    </n-carousel>
  </n-modal>
</template>
<style>
.n-carousel {
  max-width: 50vh !important;
  margin: auto;
}
.n-image-preview-toolbar {
  @apply flex gap-4;
}

.n-image img {
 width: 50%;
 object-fit: cover !important;
}

.carousel-img {
 width: 100%;
 object-fit: cover;
}
</style>
<style scoped>
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
