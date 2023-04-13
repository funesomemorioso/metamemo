<script lang="ts">
import ApiService from "@/api/apiService";
import { NDataTable, NModal, NCarousel } from "naive-ui";
import {
  defineComponent,
  ref,
  reactive,
  watch,
  onMounted,
  onBeforeUnmount,
} from "vue";

// Icons
import Download from "@vicons/carbon/Download";
import ArrowRight from "@vicons/carbon/ArrowRight";
import ArrowLeft from "@vicons/carbon/ArrowLeft";

// Types
import type { Ref } from "vue";
import type { Url } from "url";
import { useStore } from "vuex";

import { formatDateHour, formatToApi, pontuateNumber } from "../utils";
import { createColumns } from "../columnsTables";

function populateTable(
  data: {
    items: [
      {
        title: string;
        source?: string;
        content_date?: string;
        author?: string;
        url?: Url;
        image_url?: Url;
        media_urls?: Array<string>;
        context?: string;
        start_date?: string;
        end_date?: string;
        media?: string;
        transcription?: string;
        original_url?: string;
        media_url?: string;
      }
    ];
  },
  rows: Ref
) {
  const result = [];
  for (const row of data.items) {
    result.push({
      title: row.title,
      source: row.source,
      content_date: row.content_date ? formatDateHour(row.content_date) : "",
      author: row.author,
      url: row.url,
      midia: row.image_url,
      media_urls: row.media_urls,
      context: row.context,
      start_date: row.start_date,
      end_date: row.end_date,
      media: row.media,
      transcription: row.transcription,
      original_url: row.original_url,
      media_url: row.media_url,
    });
  }
  rows.value = result;
}

export default defineComponent({
  components: { NDataTable, NModal, NCarousel },
  setup() {
    const store = useStore();
    const loading = ref(true);
    const rows = ref([]);
    const paginationReactive = reactive({
      page: store.state.page,
      pageCount: 0,
      pageSize: store.state.pageSize,
      pageSizes: store.state.pageSizes,
      showSizePicker: true,
      pageSlot: 7,
    });
    const lastMutation: Ref = ref({});
    const showModalRef = ref(false);
    const modalContent = ref({ media_urls: [] });
    const columns: Ref = ref(
      createColumns(
        store.state.tab,
        store.state.sorter,
        showModalRef,
        modalContent
      )
    );
    const subscribe = ref(() => {});
    const tableRef: Ref = ref(null);
    const itemCount = ref(0);

    onMounted(async () => {
      await dataToApiRequest();
    });

    watch(
      () => [store.state.form, store.state.tab, store.state.sorter],
      async () => {
        await dataToApiRequest();

        if (lastMutation?.value?.type == "UPDATE_TAB") {
          tableRef?.value?.sort(null);
        }
      }
    );

    watch(
      () => [store.state.page, store.state.pageSize],
      async () => {
        await dataToApiRequest();
        if (lastMutation?.value?.type.startsWith("UPDATE_PAGE")) {
          document
            .querySelector(".n-data-table__pagination")
            ?.scrollIntoView({ block: "center" });
        }
      }
    );

    const pageSlotSetSize = () => {
      if (window.innerWidth < 800) {
        paginationReactive.pageSlot = 5;
        return;
      }
      paginationReactive.pageSlot = 7;
    };

    onMounted(() => {
      // Subscribe to check last mutations
      subscribe.value = store.subscribe((mutation) => {
        lastMutation.value = mutation;
      });
      pageSlotSetSize();
      window.addEventListener("resize", pageSlotSetSize);
    });

    onBeforeUnmount(() => {
      // Removing subscribe
      subscribe.value();
      window.removeEventListener("resize", pageSlotSetSize);
    });

    const dataToApiRequest = async () => {
      const form = store.state.form;
      const tab = store.state.tab;
      const page = store.state.page;
      const pageSize = store.state.pageSize;
      const sorter = store.state.sorter;

      const routerResult = formatToApi(form, page, pageSize, sorter);
      loading.value = true;
      const result: {
        items: [
          {
            title: string;
            source?: string;
            content_date?: string;
            author?: string;
            url?: Url;
            image_url?: Url;
            media_urls?: Array<string>;
            start_date?: string;
            end_date?: string;
            context?: string;
            media?: string;
            transcription?: string;
          }
        ];
        total_pages: number;
        page_size: number;
        page_page: number;
        page: number;
        total_items: number;
      } = await ApiService.get(`/${tab}/`, { ...routerResult });
      loading.value = false;

      populateTable(result, rows);
      columns.value = createColumns(
        store.state.tab,
        store.state.sorter,
        showModalRef,
        modalContent
      );

      // Update table pagination controls
      paginationReactive.page = Number(result.page);
      paginationReactive.pageCount = Number(result.total_pages);
      paginationReactive.pageSize = Number(result.page_size);
      itemCount.value = Number(pontuateNumber(result.total_items));
    };

    const handlePageChange = (currentPage: number) => {
      store.commit("UPDATE_PAGE", currentPage);
    };

    const handlePageSizeChange = (pageSize: number) => {
      store.commit("UPDATE_PAGE_SIZE", pageSize);
    };

    const handleSorterChange = (sorter: {
      columnKey: string;
      order: string;
    }) => {
      store.commit("UPDATE_SORTER", sorter);
    };

    const endsWithAny = (str: string, suffixes: Array<string>) => {
      return suffixes.some((suffix) => str.endsWith(suffix));
    };

    return {
      table: tableRef,
      data: rows,
      columns,
      loading,
      pagination: paginationReactive,
      handlePageChange,
      handlePageSizeChange,
      handleSorterChange,
      showModal: showModalRef,
      bodyStyle: {
        width: "600px",
      },
      segmented: {
        content: "soft",
      } as const,
      Download,
      ArrowLeft,
      ArrowRight,
      modalContent,
      endsWithAny,
      itemCount,
    };
  },
});
</script>

<template>
  <p
    v-if="itemCount > 0"
    class="mb-2 my-0 text-gray-600 dark:text-gray-400 text-end"
  >
    Total de itens listados:
    <span class="text-gray-700 dark:text-gray-300 font-mono">{{ itemCount }}</span>
  </p>
  <n-data-table
    ref="table"
    :pagination="pagination"
    :loading="loading"
    :columns="columns"
    :data="data"
    :scrollbar-props="{ trigger: 'none', xScrollable: true }"
    :remote="true"
    @update:page="handlePageChange"
    @update:pageSize="handlePageSizeChange"
    @update:sorter="handleSorterChange"
  />
  <n-modal
    v-model:show="showModal"
    class="custom-card"
    preset="card"
    title="Conteúdo"
    :bordered="false"
    size="huge"
    :segmented="segmented"
  >
    <n-carousel
      :dot-placement="'top'"
      :loop="false"
      :show-arrow="modalContent.media_urls.length > 1 ? true : false"
      class="carousel-img"
      draggable
    >
      <div v-for="(content, index) in modalContent.media_urls" :key="index">
        <video v-if="endsWithAny(content, ['mp4', 'mpeg', 'mkv'])" controls>
          <source :src="content" />
        </video>
        <img v-else :src="content" />
      </div>
    </n-carousel>
  </n-modal>
</template>

<style>
.n-modal.custom-card {
  width: 70vh;
}
</style>
