<script lang="ts">
import { ref, computed, watch, onBeforeMount } from "vue";
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
  startDate: any;
  endDate: any;
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
    const showSearchField = ref(true);
    const showNetworksField = ref(true);
    const showPersonsField = ref(true);

    const model = ref<Model>({
      startDate: store.state.form.startDate,
      endDate: store.state.form.endDate,
      searchText: store.state.form.searchText,
      socialMedia: store.state.form.socialMedia,
      selectedPeople: store.state.form.selectedPeople,
    });

    const peopleOptions = [
      { label: "Jair Bolsonaro", value: "Jair+Bolsonaro" },
      { label: "Carlos bolsonaro", value: "Carlos+Bolsonaro" },
      { label: "Eduardo Bolsonaro", value: "Eduardo+Bolsonaro" },
      { label: "Flavio Bolsonaro", value: "Flávio+Bolsonaro" },
      { label: "Família Bolsonaro", value: "Família+Bolsonaro" },
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

    const disableEndDatePicker = () => {
      const endDate = model.value.endDate;
      const startDate = model.value.startDate;
      const tsEndDate = endDate ? new Date(endDate) : null;
      const tsStartDate = startDate ? new Date(startDate) : null;
      if (!tsStartDate || !tsEndDate) {
        return;
      }
      if (tsStartDate > tsEndDate) {
        model.value.endDate = startDate;
        model.value.startDate = endDate;
      }
    };

    const updateFieldsForm = (tab: string) => {
      showSearchField.value = true;
      if (tab === "lista") {
        showNetworksField.value = true;
        showPersonsField.value = true;
        return;
      }
      showNetworksField.value = false;
      showPersonsField.value = false;
      if (tab === "newscovers") {
        showSearchField.value = false;
      }
    };

    watch(
      () => store.state.tab,
      (tab) => {
        updateFieldsForm(tab);
      }
    );

    onBeforeMount(() => {
      updateFieldsForm(store.state.tab);
    });

    const disablePreviousDate = (ts: number) => {
      const timestamp = Date.now();
      const dateNow = new Date(timestamp);
      const tsDate = new Date(ts);
      dateNow.setHours(23);
      dateNow.setMinutes(59);
      dateNow.setSeconds(59);
      return tsDate >= dateNow;
    };

    const handleKeyUp = async (e: KeyboardEvent) => {
      if (e.key === "Enter") {
        await submitForm();
      }
    };

    return {
      category: computed(() => store.state.tab),
      data,
      handleUpdateTab,
      model,
      peopleOptions,
      socialOptions,
      submitForm,
      disableEndDatePicker,
      showNetworksField,
      showPersonsField,
      showSearchField,
      previousMonth: getPreviousMonthTimestamp(),
      handleKeyUp,
      disablePreviousDate,
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
        class="col-span-12 lg:col-span-6 xl:col-span-3 flex"
      >
        <n-date-picker
          v-model:value="model.startDate"
          placeholder="Data Inicial"
          clearable
          :default-calendar-start-time="previousMonth"
          :update-value-on-close="true"
          :is-date-disabled="disablePreviousDate"
          class="start-datepicker"
          size="large"
          @update:value="disableEndDatePicker"
        />
        <n-date-picker
          v-model:value="model.endDate"
          placeholder="Data Final"
          clearable
          :default-calendar-start-time="previousMonth"
          :update-value-on-close="true"
          :is-date-disabled="disablePreviousDate"
          class="end-datepicker"
          size="large"
          @update:value="disableEndDatePicker"
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
        <n-form-item v-if="showSearchField" label="Pesquisa">
          <n-input
            v-model:value="model.searchText"
            size="large"
            clearable
            placeholder="Pesquise termos específicos, ex: Amazônia"
            @keyup="handleKeyUp"
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
.start-datepicker .n-input .n-input__border {
  @apply border-r-transparent;
}
.end-datepicker .n-input .n-input__border {
  @apply border-l-transparent;
}
.start-datepicker .n-input.n-input--resizable.n-input--stateful {
  @apply rounded-tr-none rounded-br-none;
}
.end-datepicker .n-input.n-input--resizable.n-input--stateful {
  @apply rounded-tl-none rounded-bl-none;
}
</style>
