<script lang="ts">
import { useMeta } from "vue-meta";
import {
  NAnchor,
  NAnchorLink,
  NAvatar,
  NCard,
  NCollapse,
  NCollapseItem,
  NH1,
  NSpin,
  NThing,
} from "naive-ui";
import { onMounted, onBeforeUnmount, ref } from "vue";
import ApiService from "@/api/apiService";
import { formatDateHour, capitalizeFirstLetter } from "../utils";

import type { Ref } from "vue";
import { useRoute, useRouter } from "vue-router";

export default {
  components: {
    NAnchor,
    NAnchorLink,
    NAvatar,
    NCard,
    NCollapse,
    NCollapseItem,
    NH1,
    NSpin,
    NThing,
  },
  setup() {
    useMeta({
      title: "Linha do tempo",
      description: "Linha do tempo dos dados catalogados",
      htmlAttrs: { lang: "pt-br", amp: true },
    });

    const router = useRouter();
    const route = useRoute();
    const timelineData: Ref = ref({});
    const loading: Ref = ref(false);
    const data:
      | Ref<[{ timeline: { image: String; name: String; title: String } }]>
      | Ref = ref([]);
    const sessionData = ref({});
    const person: Ref = ref(null);

    onMounted(async () => {
      document.querySelector("html")?.classList.add("scroll-smooth");

      const session: {
        meta: [];
        objects: [{ timeline: { image: String; name: String; title: String } }];
      } = await ApiService.get(`/timeline/api/v1/session/`, { limit: 100000 });

      sessionData.value = session.meta;
      data.value = session.objects;
    });

    onBeforeUnmount(() => {
      document.querySelector("html")?.classList.remove("scroll-smooth");
    });

    const selectPerson = async (item: {
      timeline: {
        image: string;
        name: string;
        title: string;
        start: string;
        end: string;
      };
    }) => {
      loading.value = true;
      timelineData.value = await ApiService.get(`/timeline/api/v1/fact/`, {
        limit: 100000,
        timeline__name: item.timeline.name,
      });

      router.replace({ path: route.path });
      const sortedTimelineData = timelineData.value.objects.sort((a:{date: string}, b:{date: string}) => new Date(b.date).valueOf() - new Date(a.date).valueOf());

      const timeline: any = {};

      const weekDays = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];

      for (const tDate of sortedTimelineData) {
        const date = new Date(tDate.date);
        const year = date.getFullYear();
        const month = capitalizeFirstLetter(date.toLocaleString('pt-BR', { month: 'long' }));

        const dayOfWeek = weekDays[date.getDay()];
        const day = date.getDate();

        const dayFull = `${dayOfWeek}, ${day}`;
        tDate.dayFull = dayFull;

        if (timeline[year]) {
          if (timeline[year][month]) {
            timeline[year][month].push(tDate);
          } else {
            timeline[year][month] = [tDate];
          }
        } else {
          timeline[year] = {};
          timeline[year][month] = [tDate];
        }
      }

      person.value = {
        ...item.timeline,
        start: formatDateHour(item.timeline.start, true).split("/")[2],
        end: formatDateHour(item.timeline.end, true).split("/")[2],
        description: timelineData.value.objects.find(
          (el: { date: string }) => el.date === item.timeline.start
        ),
        timeline,
      };
      loading.value = false;
      document.querySelector("#top")?.scrollIntoView({ block: "start" });
    };

    return {
      timelineData,
      sessionData,
      data,
      selectPerson,
      person,
      loading,
    };
  },
};
</script>

<template>
  <div class="p-12" style="min-height: 450px">
    <n-h1 class="pb-6">Selecione um personagem para ver a linha do tempo</n-h1>
    <div class="grid grid-cols-12 gap-4">
      <n-card
        v-for="(item, index) in data"
        :key="index"
        class="col col-span-12 lg:col-span-3 hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer"
        :class="{ 'bg-card': person && person.name == item.timeline.name }"
        @click="selectPerson(item)"
      >
        <n-thing>
          <template v-if="item.timeline.image" #avatar>
            <n-avatar
              :src="item.timeline.image"
              :size="50"
              round
              object-fit="cover"
            />
          </template>
          <template v-if="item.timeline.name" #header>
            {{ item.timeline.name }}
          </template>
          <template v-if="item.text">
            {{ item.text }}
          </template>
        </n-thing>
      </n-card>
    </div>
  </div>
  <n-spin v-if="loading || person" :show="loading">
    <section v-if="person" class="dark:text-gray-200 pt-12 pb-32">
      <div class="container px-4 py-12 grid grid-cols-12">
        <div class="grid gap-4 col-span-12 lg:grid-cols-6 lg:col-span-9">
          <div id="top" class="flex flex-col col-span-12 lg:col-span-4">
            <n-avatar
              round
              object-fit="cover"
              :size="200"
              :src="person.image"
              class="mx-auto sm:mx-0 mb-8"
            />
            <div class="text-center sm:text-left mb-14">
              <h3 class="text-3xl font-semibold">{{ person.name }}</h3>
              <span
                class="text-sm font-bold tracking-wider uppercase dark:text-gray-500"
              >
                {{ person.start }} - {{ person.end }}
              </span>
              <p class="pt-4">{{ person.description.text }}</p>
            </div>
          </div>
          <div class="relative col-span-12 px-4 space-y-6 sm:col-span-9">
            <div
              class="col-span-12 space-y-12 relative px-4 flex flex-col gap-20 sm:col-span-8 sm:space-y-8 sm:before:absolute sm:before:top-2 sm:before:bottom-0 sm:before:w-0.5 sm:before:-left-3 before:bg-gradient-to-b before:from-gray-400"
            >
              <div
                v-for="[year, months] of Object.entries(person.timeline)"
                :id="year"
                :key="year"
                class="flex flex-col sm:relative sm:before:absolute sm:before:top-2 sm:before:w-4 sm:before:h-4 sm:before:rounded-full sm:before:left-[-35px] sm:before:z-[1] before:dark:bg-primary-dark before:bg-primary-dark"
              >
              <h3 class="text-xl font-semibold tracking-wide">{{ year }}</h3>
                <div>
                  <n-collapse class="pt-8">
                    <n-collapse-item
                      v-for="[month, days] of Object.entries(months)"
                      :id="month"
                      :key="month"
                      :title="month" :name="month"
                    >
                      <n-collapse :default-expanded-names="days.map(el => el.date)">
                        <n-collapse-item
                          v-for="content in days"
                          :id="content.id"
                          :key="content.id"
                          :title="content.dayFull" :name="content.date"
                        >
                        <div>{{ content.text }}</div>
                        </n-collapse-item>
                      </n-collapse>
                    </n-collapse-item>
                  </n-collapse>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div style="width: 192px" class="sm:col-span-3 relative">
          <n-anchor :bound="150" :show-background="true" type="block">
            <n-anchor-link title="Início" href="#top" />
            <n-anchor-link
              v-for="(year, index) in Object.keys(person.timeline)"
              :key="index"
              :title="String(year)"
              :href="'#' + year"
            />
          </n-anchor>
        </div>
      </div>
    </section>
  </n-spin>
</template>

<style scoped>
.n-anchor {
  @apply sticky top-16 z-20 overflow-y-auto scrollbar invisible lg:visible;
  max-height: calc(100vh - 100px);
}

.bg-card {
  @apply bg-gray-200 dark:bg-gray-800 cursor-auto hover:bg-gray-200 dark:hover:bg-gray-800;
}
.n-spin-container {
  min-height: 200px;
}
</style>
<style>
.n-thing-header-wrapper {
  @apply flex;
}

.n-spin-container .n-spin-body {
  @apply top-0 !important;
}
</style>
