<script lang="ts">
import { ref, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { urlUpdateWithState, getPreviousMonthTimestamp } from "../utils";

import {
  NForm,
  NFormItem,
  NDatePicker,
  NInput,
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
    const showNetworksField = ref(true);
    const showPersonsField = ref(true);

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
      // Reset form fileds with new values
      model.value = {
        ...model.value,
        socialMedia: store.state.form.socialMedia,
        selectedPeople: store.state.form.selectedPeople,
      };
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

    watch(
      () => store.state.tab,
      (tab) => {
        if (tab === "lista") {
          showNetworksField.value = true;
          showPersonsField.value = true;
          return;
        }

        showNetworksField.value = false;
        showPersonsField.value = false;
      }
    );

    return {
      category: computed(() => store.state.tab),
      data,
      handleUpdateTab,
      model,
      peopleOptions,
      socialOptions,
      submitForm,
      disablePreviousDate,
      showNetworksField,
      showPersonsField,
      previousMonth: getPreviousMonthTimestamp(),
    };
  },
};
</script>

<template>
  <section>
    <n-form
      ref="form"
      :model="model"
      :class="!displayTabs ? '' : 'grid grid-cols-12 gap-x-4'"
    >
      <n-form-item
        label="Datas"
        class="col-span-12 lg:col-span-6 xl:col-span-3"
      >
        <n-date-picker
          v-model:value="model.dateRange"
          type="daterange"
          clearable
          :default-calendar-start-time="previousMonth"
          :default-calendar-end-time="Date.now()"
          start-placeholder="Data incial"
          end-placeholder="Data final"
          :update-value-on-close="true"
          :is-date-disabled="disablePreviousDate"
          size="large"
        />
      </n-form-item>
      <n-form-item
        v-if="showPersonsField"
        label="Pessoas"
        class="col-span-12 lg:col-span-6 xl:col-span-3"
      >
        <n-select
          v-model:value="model.selectedPeople"
          multiple
          filterable
          clearable
          placeholder="Selecione pessoas"
          :options="peopleOptions"
          size="large"
        />
      </n-form-item>
      <n-form-item
        v-if="showNetworksField"
        label="Plataformas"
        class="col-span-12 xl:col-span-6"
      >
        <n-select
          v-model:value="model.socialMedia"
          multiple
          filterable
          clearable
          placeholder="Selecione plataforma"
          :options="socialOptions"
          size="large"
        />
      </n-form-item>
      <div
        class="col-span-12"
        :class="showPersonsField && showNetworksField ? 'md:col-span-10' : 'md:col-span-7'"
      >
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
        <n-button size="large" type="primary" class="grow" @click="submitForm">
          Enviar
        </n-button>
      </div>
    </n-form>
    <n-tabs
      v-if="displayTabs"
      type="bar"
      :value="category"
      size="large"
      justify-content="center"
      class="mt-2"
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

<style>
.n-date-panel {
  @apply flex flex-col sm:grid !important;
}
.v-binder-follower-content {
  @apply z-40;
}
</style>
