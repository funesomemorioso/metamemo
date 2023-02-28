<script lang="ts">
import { defineComponent, ref, reactive, watch, h, onMounted, toRef } from 'vue';
import { useRoute } from 'vue-router';
import { NDataTable, NButton, NIcon, NText, NModal, NImage } from 'naive-ui';
import { useMeta } from "vue-meta"

// Icons
import Link from '@vicons/carbon/Link';
import Image from '@vicons/carbon/Image';
import LogoTwitter from '@vicons/carbon/LogoTwitter';
import LogoFacebook from '@vicons/carbon/LogoFacebook';
import TelegramTwotone from '@vicons/material/TelegramTwotone';
import LogoInstagram from '@vicons/carbon/LogoInstagram';
import LogoYoutube from '@vicons/carbon/LogoYoutube';
import Blogger from '@vicons/fa/Blogger';

// Types
import type { DataTableColumns } from 'naive-ui';
import type { Ref } from 'vue';
import type { Url } from 'url';

const emptyResult = h(NText, { depth: 3, italic: true }, { default: () => '(vazio)' });

function linkify(text: string): string {
  const urlRegex = /((?:https?:\/\/)[^\s]+)/g;
  return text.replace(urlRegex, '<a class="font-semibold hover:underline underline-offset-4" href="$1">$1</a>');
}

function formatDateHour(
  dateHourUTC: string,
  locale: string = 'pt-BR',
  separatorString: string = 'às'
) {
  const dateHour = new Date(dateHourUTC);
  const dateFormated = dateHour.toLocaleDateString(locale);
  const hourFormated = dateHour.toLocaleTimeString(locale);
  return `${dateFormated} ${separatorString} ${hourFormated}`;
}

function parseDateString(dateString: string): Date {
  const [datePart, timePart] = dateString.split(' às ');
  const [day, month, year] = datePart.split('/').map(Number);
  const [hours, minutes, seconds] = timePart.split(':').map(Number);
  const date = new Date(year, month - 1, day, hours, minutes, seconds);
  return date;
}

function populateTable(
  data: {
    items: [
      {
        title: string,
        source: string,
        content_date: string,
        author: string,
        url: Url,
        image_url: Url
      }
    ]
  },
  rows: Ref
) {
  const result = [];
  for (const row of data.items) {
    result.push(
      {
        title: row.title,
        source: row.source,
        "date": formatDateHour(row.content_date),
        author: row.author,
        url: row.url,
        midia: row.image_url
      })
  }
  rows.value = result;
}

const createColumns = (): DataTableColumns => {
  return [
    {
      title: 'Conteúdo',
      key: 'title',
      width: 400,
      sorter: true,
      render(row) {
        const title = row.title;
        if (!title) {
          return emptyResult;
        }
        return h(
          "div", {
            class: "h-42 p-2 rounded transition ease-in-out hover:bg-sky-100 dark:hover:bg-gray-700 hover:shadow",
            innerHTML: `${linkify(String(title))}`,
        }
        )
      }
    },
    {
      title: 'Rede',
      key: 'source',
      width: 100,
      render(row) {
        let url = row.url;
        const source = row.source;

        // Define icon and icon color
        let sourceIcon = { icon: Link, color: 'text-gray-600' }

        if (source == 'Twitter') {
          sourceIcon = { icon: LogoTwitter, color: 'text-sky-600 dark:text-sky-500' }
        }
        else if (source == 'Telegram') {
          url = row.midia
          sourceIcon = { icon: TelegramTwotone, color: 'text-gray-500 dark:text-gray-400' }
        }
        else if (source == 'Youtube') {
          sourceIcon = { icon: LogoYoutube, color: 'text-rose-600 dark:text-rose-500' }
        }
        else if (source == 'Facebook') {
          sourceIcon = { icon: LogoFacebook, color: 'text-blue-600 dark:text-blue-500' }
        }
        else if (source == 'Instagram') {
          sourceIcon = { icon: LogoInstagram, color: 'text-pink-600 dark:text-pink-500' }
        }
        else if (source == 'Blog') {
          sourceIcon = { icon: Blogger, color: 'text-orange-600 dark:text-orange-500' }
        }

        return h(
          NButton,
          {
            strong: true,
            secondary: true,
            style: 'padding: 8px',
            title: url,
            onClick: () => { window.open(String(url), '_blank') },
          },
          () => h(NIcon,
            {
              size: '1.12rem',
              class: sourceIcon.color,
              component: h(sourceIcon.icon),
            }
          )
        )
      }
    },
    {
      title: 'Data e Hora',
      key: 'date',
      width: 220,
      sorter: true,
    },
    {
      title: 'Autor',
      key: 'author',
      width: 220,
      sorter: true
    },
    {
      title: 'Midia',
      key: 'midia',
      width: 220,
      render(row) {
        const midia = row.midia;
        if (!midia) {
          return emptyResult;
        }
        return [h(
          NButton,
          {
            strong: true,
            secondary: true,
            style: 'padding: 8px',
            title: midia,
            onClick: () => {
              window.open(
                String(midia),
                '_blank',
                'location=yes,width=1024,scrollbars=yes,status=yes'
              )
            }
          },
          () => h(NIcon,
            {
              size: '1.12rem',
              component: h(Image),
            }
          )
        )
        ]
      }
    }
  ]
}

export default defineComponent({
  props: ['data', 'loading'],
  components: { NDataTable, NButton, NModal, NImage },
  setup(props, context) {
    const route = useRoute()

    useMeta({
      title: 'Consulta',
      description: 'Página de consulta de dados metamemo com formulários para filtragem de conteúdo extraído',
      htmlAttrs: { lang: 'pt-br', amp: true }
    })

    const loading = toRef(props, 'loading');
    const rows = ref([]);
    const paginationReactive = reactive({
      page: 1,
      pageCount: 10,
      pageSize: 5,
      pageSizes: [5, 10, 20, 50, 100],
      showSizePicker: true
    })

    watch(
      () => props.data, (data) => {
        populateTable(data, rows)
        paginationReactive.pageCount = props.data.total_pages
        paginationReactive.pageSize = props.data.page_size
        paginationReactive.page = props.data.page
      }
    )

    const handlePageChange = (currentPage: number) => {
      context.emit('paginateAction', currentPage)
    }

    const handlePageSizeChange = (pageSize: number) => {
      context.emit('paginateSizeAction', pageSize)
    }

    const handleSorterChange = (sorter: { [key: string] : any }) => { 
      context.emit('sortAction', sorter)
    }

    return {
      data: rows,
      columns: createColumns(),
      loading,
      pagination: paginationReactive,
      handlePageChange,
      handlePageSizeChange,
      handleSorterChange
    }
  },
})
</script>

<template>
  <n-data-table
    :pagination="pagination"
    :loading="loading"
    :columns="columns"
    :data="data"
    :scrollbar-props="{ trigger: 'none', 'xScrollable': true }" :remote="true" @update:page="handlePageChange"
    @update:pageSize="handlePageSizeChange"
    @update:sorter="handleSorterChange"
  />
</template>

<style>
.n-date-panel {
  @apply flex flex-col sm:grid !important;
}
tbody .n-data-table-tr {
  @apply h-52;
}
</style>
