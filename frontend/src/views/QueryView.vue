<script lang="ts">
import { defineComponent, ref, reactive, onMounted, h } from 'vue';
import type { Ref } from 'vue';
import { NDataTable, NButton, NIcon } from 'naive-ui';
import Link from '@vicons/carbon/Link';
import Image from '@vicons/carbon/Image';
import LogoTwitter from '@vicons/carbon/LogoTwitter';
import LogoFacebook from '@vicons/carbon/LogoFacebook';
import TelegramTwotone from '@vicons/material/TelegramTwotone';
import LogoInstagram from '@vicons/carbon/LogoInstagram';
import LogoYoutube from '@vicons/carbon/LogoYoutube';
import type { DataTableColumns } from 'naive-ui';


const createColumns = (): DataTableColumns => {
  return [
    {
      title: 'Title',
      key: 'title',
      resizable: true,
      minWidth: 300,
      width: 500,
    },
    {
      title: 'Rede',
      key: 'source',
      width: 100,
      render (row) {
        let url = row.url;
        const source = row.source;

        let sourceIcon = { icon: Link, color: 'text-gray-600' }
        console.log(source)
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

        return h(
          NButton,
          {
            strong: true,
            secondary: true,
            style: 'padding: 8px',
            title: url,
            onClick: () => { window.open(String(url), '_blank') },
          },
          { default:
            () => h(NIcon,
              {
                size: '1.12rem',
                class: sourceIcon.color,
                component: () => h(sourceIcon.icon),
              }
            )
          }
        )
      }
    },
    {
      title: 'Data e Hora',
      key: 'date',
      width: 220,
    },
    {
      title: 'Autor',
      key: 'author',
      width: 220,
    },
    {
      title: 'Midia',
      key: 'midia',
      width: 220,
      render (row) {
        const midia = row.midia;
        if (!midia) {
          return;
        }
        return h(
          NButton,
          {
            strong: true,
            secondary: true,
            style: 'padding: 8px',
            title: midia,
            onClick: () => { window.open(String(midia), '_blank') },
          },
          { default:
            () => h(NIcon,
              {
                size: '1.12rem',
                component: () => h(Image),
              }
            )
          }
        )
      }
    },
  ]
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


export default defineComponent({
  components: { NDataTable, NButton },
  setup() {
    const rows: [] | Ref = ref([]);
    const loading = ref(true);
    const paginationReactive = reactive({
      page: 1,
      pageSize: 5,
      pageSlot: 7,
      showSizePicker: true,
      simple: window.innerWidth < 480 ? true : false,
      pageSizes: [5, 10, 20, 50],
      onChange: (page: number) => {
        paginationReactive.page = page
      },
      onUpdatePageSize: (pageSize: number) => {
        paginationReactive.pageSize = pageSize
        paginationReactive.page = 1
      }
    })

    onMounted(async () => {
      loading.value = true;
      try {
        const api = import.meta.env.VITE_API_URL
        const response = await fetch(api + '/lista/?author=Jair%20Bolsonaro&author=Carlos%20Bolsonaro&author=Eduardo%20Bolsonaro&author=Fl%C3%A1vio%20Bolsonaro&author=Familia%20Bolsonaro&source=Facebook&source=Twitter&source=Youtube&source=Instagram&source=Telegram&source=Blog&content=&start_date=2023-2-1&end_date=2023-2-28&format=json');
        const data = await response.json();
        const result = [];
        for (const row of data.items) {
          result.push(
            {
              title:  row.title,
              source: row.source,
              "date": formatDateHour(row.content_date),
              author: row.author,
              url: row.url,
              midia: row.image_url
            })
        }
        rows.value = result;
      } catch (error) {
        console.error(error);
      }
        loading.value = false;
    });

    return {
      data: rows,
      columns: createColumns(),
      loading,
      pagination: paginationReactive,
      scroll
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
      :scrollbar-props="{ trigger: 'none', 'xScrollable': true }"
    />
</template>

<style>
</style>
