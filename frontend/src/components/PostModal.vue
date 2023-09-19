<script lang="ts">
import View from '@vicons/carbon/View';
import ThumbsUpFilled from '@vicons/carbon/ThumbsUpFilled';
import { defineComponent, watch, ref, computed } from "vue";
import { useStore } from "vuex";
import { NModal, NCarousel, NImage, NScrollbar, NIcon } from "naive-ui";
import type { Ref } from "vue";
import noData from '../assets/no-data.svg'
import { formatNumberSuffix } from '@/utils';

export default defineComponent({
  components: { NModal, NCarousel, NImage, NScrollbar, NIcon },
  setup() {
    const store = useStore();
    const showModal = ref(false);
    const content: Ref = ref({ text: '', likes: 0, views: 0, media_urls: [], media_url: null });

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

    const handleCloseModal = () => {
      const imgPreview = document.querySelector('.n-image-preview-container');
      // If imgPreview active don`t close modal
      if (imgPreview) {
        return
      }
      showModal.value = false
    }

    return {
      handleCloseModal,
      showModal,
      dateTime,
      content,
      text,
      endsWithAny,
      bodyStyle: computed(() => {
        return { width: content.value.media_url ? "800px" : "600px" }
      }),
      handleCloseButton,
      noData,
      View,
      ThumbsUpFilled,
      formatNumberSuffix
    };
  },
});
</script>

<template>
  <n-modal
    v-model:show="showModal"
    class="custom-card"
    preset="card"
    title="Publicação"
    :style="bodyStyle"
    :bordered="false"
    :close-on-esc="false"
    size="medium"
    transform-origin="center"
    :on-esc="handleCloseModal"
  >
    <template #header-extra>
      <section class="header-content">
        <span>
          {{ dateTime }}
        </span>
      </section>
    </template>

    <n-scrollbar class="custom-card-body">
      <div
        v-if="content.media_url"
        class="pb-8 flex gap-2 h-96"
      >
        <n-carousel
          :dot-placement="'top'"
          :loop="false"
          class="bg-gray-500 dark:bg-zinc-700 rounded"
          draggable
        >
          <video v-if="endsWithAny(content.media_url, ['mp4', 'mpeg', 'mkv'])" controls>
            <source :src="content.media_url" />
          </video>
          <n-image
            v-else
            :src="content.media_url"
            :fallback-src="noData"
          />
        </n-carousel>
      </div>
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
              :fallback-src="noData"
            />
          </template>
        </n-carousel>
      </div>
    </n-scrollbar>
    <template #footer>
      <section class="footer-modal">
        <div v-if="content.views > 0" class="number-element whitespace-nowrap" title="Visualizações">
          <n-icon :component="View" />
          {{ formatNumberSuffix(content.views) }}
        </div>
        <div v-if="content.likes > 0" class="number-element whitespace-nowrap" title="Likes">
          <n-icon :component="ThumbsUpFilled" />
          {{ formatNumberSuffix(content.likes) }}
        </div>
      </section>
    </template>
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

.custom-card-body.n-scrollbar {
  @apply p-0;
}

.custom-card.n-card .n-scrollbar-content {
  @apply p-6;
}

.custom-card.n-card > .n-card__content {
  @apply p-0;
}

.custom-card .n-card-header {
  @apply border-b dark:border-gray-700;
}

.custom-card .n-card__footer {
  @apply border-t dark:border-gray-700;
}

.n-image-preview-toolbar {
  @apply flex gap-5;
}

.custom-card .n-carousel__slide {
  @apply flex justify-center;
}

.custom-card .n-image img {
  object-fit: contain !important;
}

.n-modal-mask {
  @apply backdrop-blur-sm;
}

.custom-card-body {
  max-height: calc(100vh - 170px);
  overflow-y: auto;
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

.footer-modal {
  @apply flex justify-end gap-2 pt-4 items-center;
}

.number-element {
  @apply flex gap-2 items-center border border-gray-500 px-4 py-1 rounded-2xl;
}
</style>
