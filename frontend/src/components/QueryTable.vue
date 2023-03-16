<script lang="ts">
import ApiService from "@/api/apiService";
import { NDataTable, NButton, NIcon, NText, NModal, NImage } from "naive-ui";
import {
  defineComponent,
  ref,
  reactive,
  watch,
  h,
  onMounted,
  onBeforeUnmount,
} from "vue";

// Icons
import Blogger from "@vicons/fa/Blogger";
import Image from "@vicons/carbon/Image";
import Link from "@vicons/carbon/Link";
import LogoFacebook from "@vicons/carbon/LogoFacebook";
import LogoInstagram from "@vicons/carbon/LogoInstagram";
import LogoTwitter from "@vicons/carbon/LogoTwitter";
import LogoYoutube from "@vicons/carbon/LogoYoutube";
import TelegramTwotone from "@vicons/material/TelegramTwotone";

// Types
import type { DataTableColumns } from "naive-ui";
import type { Ref } from "vue";
import type { Url } from "url";
import { useStore } from "vuex";

import { formatDateHour, formatToApi } from "../utils";
import type { SortOrder } from "naive-ui/es/data-table/src/interface";

const emptyResult = h(
  NText,
  { depth: 3, italic: true },
  { default: () => "(vazio)" }
);

function linkify(text: string): string {
  const urlRegex = /((?:https?:\/\/)[^\s]+)/g;
  return text.replace(
    urlRegex,
    '<a class="font-semibold hover:underline underline-offset-4" href="$1" target="_blank">$1</a>'
  );
}

function populateTable(
  data: {
    items: [
      {
        title: string;
        source: string;
        content_date: string;
        author: string;
        url: Url;
        image_url: Url;
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
      content_date: formatDateHour(row.content_date),
      author: row.author,
      url: row.url,
      midia: row.image_url,
    });
  }
  rows.value = result;
}

const createColumns = (sorter: {
  columnKey: string;
  order: SortOrder;
}): DataTableColumns => {
  return [
    {
      title: "Conteúdo",
      key: "title",
      width: 400,
      sorter: true,
      sortOrder: sorter?.columnKey === "title" ? sorter.order : undefined,
      render(row) {
        const title = row.title;
        if (!title) {
          return emptyResult;
        }
        return h("div", {
          class:
            "p-2 rounded transition ease-in-out hover:bg-sky-100 dark:hover:bg-gray-700 hover:shadow",
          innerHTML: `${linkify(String(title))}`,
        });
      },
    },
    {
      title: "Rede",
      key: "source",
      width: 100,
      render(row) {
        let url = row.url;
        const source = row.source;

        // Define icon and icon color
        let sourceIcon = { icon: Link, color: "text-gray-600" };

        if (source == "Twitter") {
          sourceIcon = {
            icon: LogoTwitter,
            color: "text-sky-600 dark:text-sky-500",
          };
        } else if (source == "Telegram") {
          url = row.midia;
          sourceIcon = {
            icon: TelegramTwotone,
            color: "text-gray-500 dark:text-gray-400",
          };
        } else if (source == "Youtube") {
          sourceIcon = {
            icon: LogoYoutube,
            color: "text-rose-600 dark:text-rose-500",
          };
        } else if (source == "Facebook") {
          sourceIcon = {
            icon: LogoFacebook,
            color: "text-blue-600 dark:text-blue-500",
          };
        } else if (source == "Instagram") {
          sourceIcon = {
            icon: LogoInstagram,
            color: "text-pink-600 dark:text-pink-500",
          };
        } else if (source == "Blog") {
          sourceIcon = {
            icon: Blogger,
            color: "text-orange-600 dark:text-orange-500",
          };
        }

        return h(
          NButton,
          {
            strong: true,
            secondary: true,
            style: "padding: 8px",
            title: url,
            onClick: () => {
              window.open(String(url), "_blank");
            },
          },
          () =>
            h(NIcon, {
              size: "1.12rem",
              class: sourceIcon.color,
              component: h(sourceIcon.icon),
            })
        );
      },
    },
    {
      title: "Data e Hora",
      key: "content_date",
      width: 220,
      sorter: true,
      sortOrder:
        sorter?.columnKey === "content_date" ? sorter.order : undefined,
    },
    {
      title: "Autor",
      key: "author",
      width: 220,
      sorter: true,
      sortOrder: sorter?.columnKey === "author" ? sorter.order : undefined,
    },
    {
      title: "Midia",
      key: "midia",
      width: 220,
      render(row) {
        const midia = row.midia;
        if (!midia) {
          return emptyResult;
        }
        return [
          h(
            NButton,
            {
              strong: true,
              secondary: true,
              style: "padding: 8px",
              title: midia,
              onClick: () => {
                window.open(
                  String(midia),
                  "_blank",
                  "location=yes,width=1024,scrollbars=yes,status=yes"
                );
              },
            },
            () =>
              h(NIcon, {
                size: "1.12rem",
                component: h(Image),
              })
          ),
        ];
      },
    },
  ];
};

export default defineComponent({
  components: { NDataTable, NButton, NModal, NImage },
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
    });
    const lastMutation: Ref = ref({});
    const columns: Ref = ref(createColumns(store.state.sorter));
    const subscribe = ref(() => {});
    const tableRef: Ref = ref(null);

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

    onMounted(() => {
      subscribe.value = store.subscribe((mutation) => {
        lastMutation.value = mutation;
      });
    });

    onBeforeUnmount(() => {
      subscribe.value();
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
            source: string;
            content_date: string;
            author: string;
            url: Url;
            image_url: Url;
          }
        ];
        total_pages: number;
        page_size: number;
        page_page: number;
        page: number;
      } = await ApiService.get(`/${tab}/`, { ...routerResult });
      loading.value = false;

      populateTable(result, rows);
      columns.value = createColumns(store.state.sorter);

      // Update table pagination controls
      paginationReactive.page = Number(result.page);
      paginationReactive.pageCount = Number(result.total_pages);
      paginationReactive.pageSize = Number(result.page_size);
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
    };
  },
});
</script>

<template>
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
</template>

<style>
.n-date-panel {
  @apply flex flex-col sm:grid !important;
}
</style>
