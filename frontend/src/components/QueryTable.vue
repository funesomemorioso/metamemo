<script lang="ts">
import ApiService from "@/api/apiService";
import { NDataTable, NButton } from "naive-ui";
import {
  defineComponent,
  ref,
  reactive,
  watch,
  onMounted,
  onBeforeUnmount,
  computed,
} from "vue";
import PostModal from "./PostModal.vue";

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
        likes?: string;
        interactions?: string;
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
      likes: row.likes,
      views: row.interactions,
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
  components: { NDataTable, PostModal, NButton },
  setup() {
    const store = useStore();
    const loading = ref(true);
    const rows = ref([]);
    const tab = computed(() => store.state.tab);
    const paginationReactive = reactive({
      page: store.state.page,
      pageCount: 0,
      pageSize: store.state.pageSize,
      pageSizes: store.state.pageSizes,
      showSizePicker: true,
      pageSlot: 7,
    });
    const setPostModal = (payload: object) => {
      console.log(payload)
    };
    const lastMutation: Ref = ref({});
    const modalContent = ref({ media_urls: [] });
    const columns: Ref = ref(
      createColumns(store.state.tab, store.state.sorter, setPostModal)
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
        // TODO: Save table data in store.state to avoid cache erros like need to clear colums.value
        columns.value = [];
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
      const setPostModal = (payload: object) => {
        store.commit("UPDATE_POST_MODAL", payload);
      };
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
        setPostModal
      );

      // Update table pagination controls
      paginationReactive.page = Number(result.page);
      paginationReactive.pageCount = Number(result.total_pages);
      paginationReactive.pageSize = Number(result.page_size);
      itemCount.value = Number(pontuateNumber(result.total_items));
    };

    const downloadDataAsCsv = async () => {
      const form = store.state.form;
      const page = store.state.page;
      const pageSize = store.state.pageSize;
      const sorter = store.state.sorter;
      const params = formatToApi(form, page, pageSize, sorter);
      const queryFilters = ApiService.formatQuery({ params, format: "csv" })
      const url = `${import.meta.env.VITE_API_URL}/lista/${queryFilters}`;

      window.open(url, '_blank');
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

    return {
      table: tableRef,
      data: rows,
      columns,
      loading,
      pagination: paginationReactive,
      handlePageChange,
      handlePageSizeChange,
      handleSorterChange,
      Download,
      ArrowLeft,
      ArrowRight,
      modalContent,
      itemCount,
      downloadDataAsCsv,
      tab,
    };
  },
});
</script>

<template>

  <div class="grid grid-flow-col">
    <div v-if="itemCount > 0 && tab === 'lista'" class="mb-2">
      <n-button @click="downloadDataAsCsv()" title ="Baixar como CSV">Baixar resultado</n-button>
    </div>
    <p
      v-if="itemCount > 0"
      class="mb-2 text-gray-600 dark:text-gray-400 justify-self-end gap-2"
    >
      Total de itens listados:
      <span class="text-gray-700 dark:text-gray-300 font-mono">
        {{ itemCount }}
      </span>
    </p>
  </div>
  <n-data-table
    ref="table"
    :pagination="pagination"
    :loading="loading"
    :columns="columns"
    :data="data"
    :scrollbar-props="{ trigger: 'none', xScrollable: true }"
    :remote="true"
    @update:page="handlePageChange"
    @update:page-size="handlePageSizeChange"
    @update:sorter="handleSorterChange"
  />
  <PostModal />
</template>
