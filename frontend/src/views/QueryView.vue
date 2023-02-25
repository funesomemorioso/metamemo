<script lang="ts">
  import QueryTable from '../components/QueryTable.vue'
  import { onMounted, ref } from 'vue'; 
  import { NForm, NFormItem, NDatePicker, NInput, NCheckboxGroup, NCheckbox, NSelect, NButton } from 'naive-ui';

  function formatDate(timestamp: number): string {
    const date = new Date(timestamp);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    return `${year}-${month}-${day}`;
  }

  export default {
    components: { QueryTable, NForm, NFormItem, NDatePicker, NInput, NCheckboxGroup, NCheckbox, NSelect, NButton },
    setup() {
      const data = ref(null);
      const loading = ref(true);
      const api = import.meta.env.VITE_API_URL

      onMounted(async () => {
        try {
          loading.value = true
          const response = await fetch(
            api + '/lista/?author=Jair+Bolsonaro&source=Facebook&start_date=2023-1-24&end_date=2023-2-19&format=json'
          );
          data.value = await response.json();
          loading.value = false
        } catch (error) {
          // Do nothing
          console.error(error);
        }
      })

      const model = ref(
        {
          dateRange: null,
          searchText: "",
          socialMedia: [],
          selectedPeople: [],
        }
      )

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
        const authors = [...form.selectedPeople].map(el => `&author=${el}`).join("")
        const sources = [...form.socialMedia].map(el => `&source=${el}`).join("")
        const content = `&content=${form.searchText}`

        let startDate = ""
        let endDate = "" 

        if (form.dateRange) {
          startDate = `&start_date=${formatDate(form.dateRange[0])}`
          endDate = `&end_date=${formatDate(form.dateRange[1])}`
        }
        let query = content + authors + sources + startDate + endDate
        query = query.substring(1)
        console.log(query)

        loading.value = true;
        const response = await fetch(api + `/lista/?${query}&format=json`)
        data.value = await response.json();
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
