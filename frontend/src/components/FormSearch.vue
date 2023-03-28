<script lang="ts">
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { urlUpdateWithState } from "../utils";

import {
  NForm,
  NFormItem,
  NDatePicker,
  NInput,
  NCheckboxGroup,
  NCheckbox,
  NSelect,
  NButton,
  NTabs,
  NTabPane,
} from "naive-ui";

interface Model {
  dateRange: any;
  searchText: any;
  socialMedia: any;
  selectedPeople: any;
}

export default {
  components: {
    NForm,
    NFormItem,
    NDatePicker,
    NInput,
    NCheckboxGroup,
    NCheckbox,
    NSelect,
    NButton,
    NTabs,
    NTabPane,
  },
  props: {
    displayTabs: {
      default: true,
      type: Boolean,
    },
  },
  setup(props) {
    const store = useStore();
    const data = ref(null);
    const router = useRouter();

    const model = ref<Model>({
      dateRange: store.state.form.dateRange,
      searchText: store.state.form.searchText,
      socialMedia: store.state.form.socialMedia,
      selectedPeople: store.state.form.selectedPeople,
    });

    const peopleOptions = [
      { label: "Jair Bolsonaro", value: "Jair+Bolsonaro" },
      { label: "Carlos bolsonaro", value: "Carlos+Bolsonaro" },
      { label: "Eduardo Bolsonaro", value: "Eduardo+Bolsonaro" },
      { label: "Flavio Bolsonaro", value: "Flávio+Bolsonaro" },
      { label: "Família Bolsonaro", value: "Familia+Bolsonaro" },
    ];
    const socialOptions = [
      { label: "Facebook", value: "Facebook" },
      { label: "Instagram", value: "Instagram" },
      { label: "Twitter", value: "Twitter" },
      { label: "Youtube", value: "Youtube" },
      { label: "Telegram", value: "Telegram" },
      { label: "Blog", value: "Blog" },
    ];

    const handleUpdateTab = async (name: string) => {
      store.commit("UPDATE_TAB", name);
    };

    const submitForm = async () => {
      const form = model.value;
      store.commit("UPDATE_FORM", { ...form });
      // Front page will push to route
      if (!props.displayTabs) {
        router.push(await urlUpdateWithState(store));
      }
    };

    const disablePreviousDate = (ts: number) => {
      return ts > Date.now();
    };

    return {
      category: computed(() => store.state.tab),
      data,
      handleUpdateTab,
      model,
      peopleOptions,
      socialOptions,
      submitForm,
      disablePreviousDate,
    };
  },
};
</script>

<template>
  <section>
    <n-form ref="form" :model="model" :class="!displayTabs ? '' : 'grid grid-cols-12 gap-x-4'">
      <div class="col-span-12 lg:col-span-6 xl:col-span-3">
        <n-form-item label="Datas">
          <n-date-picker
            v-model:value="model.dateRange"
            type="daterange"
            clearable
            start-placeholder="Data incial"
            end-placeholder="Data final"
            :update-value-on-close="true"
            :is-date-disabled="disablePreviousDate"
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
        <n-form-item label="Redes">
          <n-checkbox-group
            v-model:value="model.socialMedia"
            class="flex flex-wrap gap-y-2"
          >
            <n-checkbox
              v-for="option in socialOptions"
              :label="option.label"
              :value="option.value"
            />
          </n-checkbox-group>
        </n-form-item>
      </div>
      <div class="col-span-12 md:col-span-10">
        <n-form-item label="Pesquisa">
          <n-input
            v-model:value="model.searchText"
            size="large"
            clearable
            placeholder="Pesquise termos específicos, ex: Amazônia"
          />
        </n-form-item>
      </div>
      <div
        class="col-span-12 md:col-span-2 flex flex-grow justify-center items-center"
      >
        <n-button size="large" type="primary" class="grow" @click="submitForm"
          >Enviar</n-button
        >
      </div>
    </n-form>
    <n-tabs
      v-if="displayTabs"
      type="bar"
      :value="category"
      size="large"
      justify-content="center"
      class="mb-3"
      @update:value="handleUpdateTab"
    >
      <n-tab-pane name="lista" tab="Lista"></n-tab-pane>
      <n-tab-pane name="transcricao" tab="Transcrição"></n-tab-pane>
      <n-tab-pane name="news" tab="Notícias"></n-tab-pane>
      <n-tab-pane name="contexts" tab="Contexto histórico"></n-tab-pane>
      <n-tab-pane name="newscovers" tab="Capas de jornais"></n-tab-pane>
    </n-tabs>
  </section>
</template>

<style></style>
