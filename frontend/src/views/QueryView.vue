<script lang="ts">
  import QueryTable from '../components/QueryTable.vue'
  import { onMounted, ref } from 'vue';
  import { NForm, NFormItem, NDatePicker, NInput, NCheckboxGroup, NCheckbox, NSelect, NButton } from 'naive-ui';
  import { useRoute, useRouter, type LocationQueryValue } from 'vue-router';

  function formatDate(timestamp: number): string {
    const date = new Date(timestamp);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    return `${year}-${month}-${day}`;
  }

  function convertToUtc(dateString: string): number {
    const [year, month, day] = dateString.split('-').map(Number);
    const utcDate = Date.UTC(year, month - 1, day);
    return utcDate;
  }

  interface Model {
    dateRange: any;
    searchText: any;
    socialMedia: any;
    selectedPeople: any; 
  }

  export default {
    components: { QueryTable, NForm, NFormItem, NDatePicker, NInput, NCheckboxGroup, NCheckbox, NSelect, NButton },
    setup() {
      const route = useRoute()
      const routeArgs = route.query

      const router = useRouter()
      const routerQuery = router.currentRoute.value.fullPath

      const data = ref(null);
      const loading = ref(true);
      const api = import.meta.env.VITE_API_URL

      const model = ref<Model>(
        {
          dateRange: routeArgs.start_date ?
            [ convertToUtc(String(routeArgs.start_date)), convertToUtc(String(routeArgs.end_date)) ] : null,
          searchText: routeArgs.content ? routeArgs.content : "",
          socialMedia: Array.isArray(routeArgs.source) ? routeArgs.source : routeArgs.source ? [routeArgs.source] : [],
          selectedPeople: Array.isArray(routeArgs.author) ? routeArgs.author : routeArgs.author ? [routeArgs.author] : [],
        }
      )


      onMounted(async () => {
        try {
          loading.value = true
          const resultPath =
            routerQuery.replace(String(router.currentRoute.value.path), "").replace("%2B", "+")
          let response;
          if (resultPath) {
            response = await fetch(
              `${api}/lista/${resultPath}&format=json`
            );
          } else {
            //response = await fetch(`${api}/lista/?format=json`);
            response = await fetch(`${api}/lista/?author=Jair+Bolsonaro&source=Blog&source=Facebook&format=json`);
          }
          data.value = await response.json();
          loading.value = false
        } catch (error) {
          // Do nothing
          // console.error(error);
          loading.value = false
        }
      })

      const peopleOptions = [
        { label: 'Jair Bolsonaro', value: 'Jair+Bolsonaro' },
        { label: 'Carlos bolsonaro', value: 'Carlos+Bolsonaro' },
        { label: 'Eduardo Bolsonaro', value: 'Eduardo+Bolsonaro' },
        { label: 'Família Bolsonaro', value: 'Familia+Bolsonaro' },
      ];

      const socialOptions = [
        { label: 'Facebook', value: 'Facebook' },
        { label: 'Instagram', value: 'Instagram' },
        { label: 'Twitter', value: 'Twitter' },
        { label: 'Youtube', value: 'Youtube' },
        { label: 'Telegram', value: 'Telegram' },
        { label: 'Blog', value: 'Blog' }
      ];

      const submitForm = async () => {
        const form = model.value
        const routerResult: {
          author?: LocationQueryValue[],
          source?: LocationQueryValue[],
          content?: LocationQueryValue[] | string
          start_date?: string
          end_date?: string
          } = {}

        let author: LocationQueryValue[] | string = [...form.selectedPeople]
        if (author.length > 0) {
            routerResult.author = author
            author = author.map(el => `&author=${el}`).join("")
        }

        let source: LocationQueryValue[] | string = [...form.socialMedia]
        if (source.length > 0) {
          routerResult.source = source
          source = source.map(el => `&source=${el}`).join("")
        }

        let content = form.searchText
        if(content) {
          routerResult.content = content
          content = `&content=${content}`
        }

        let startDate = ""
        let endDate = ""

        if (form.dateRange) {
          startDate = formatDate(form.dateRange[0])
          endDate = formatDate(form.dateRange[1])

          routerResult.start_date = startDate
          routerResult.end_date = endDate

          startDate = `&start_date=${startDate}`
          endDate = `&end_date=${endDate}`
        }
        let query = content + author + source + startDate + endDate
        query = query.substring(1)

        loading.value = true;
        const response = await fetch(api + `/lista/?${query}&format=json`)
        data.value = await response.json();

        router.push({ query: routerResult })
        loading.value = false;
      }

      return {
        data,
        model,
        peopleOptions,
        socialOptions,
        submitForm,
        loading
      }
    }
  }
</script>

<template>
  <n-form ref="form" :model="model" class="mb-6 grid grid-cols-12 gap-x-4">
    <div class="col-span-12 lg:col-span-6 xl:col-span-3">
      <n-form-item label="Datas">
        <n-date-picker
          type="daterange"
          start-placeholder="Data incial"
          end-placeholder="Data final"
          v-model:value="model.dateRange"
          :update-value-on-close="true"
        />
      </n-form-item>
    </div>
    <div class="col-span-12 lg:col-span-6 xl:col-span-3">
      <n-form-item label="Pessoas">
        <n-select
          v-model:value="model.selectedPeople"
          multiple
          filterable
          clearable
          placeholder="Selecione pessoas"
          :options="peopleOptions"
        />
      </n-form-item>
    </div>
    <div class="col-span-12 xl:col-span-6">
      <n-form-item label="Redes sociais">
        <n-checkbox-group  v-model:value="model.socialMedia" class="flex flex-wrap gap-y-2">
            <n-checkbox v-for="(option) in socialOptions" :label="option.label" :value="option.value" />
        </n-checkbox-group>
      </n-form-item>
    </div>
    <div class="col-span-12 md:col-span-10">
      <n-form-item label="Pesquisa">
        <n-input v-model:value="model.searchText" size="large" placeholder="Procure por termos específicos, ex: Amazônia" />
      </n-form-item>
    </div>
    <div class="col-span-12 md:col-span-2 flex flex-grow justify-center items-center">
      <n-button @click="submitForm" size="large" type="success" class="grow">Enviar</n-button>
    </div>
  </n-form>
  <QueryTable :loading="loading" :data="data" />
</template>

<style>
</style>
