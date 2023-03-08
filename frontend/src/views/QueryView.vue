<script lang="ts">
import FormSearch from "../components/FormSearch.vue"
import QueryTable from "../components/QueryTable.vue"
import { onBeforeUnmount, watch, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import { formatToApi, convertDateToUtc } from "../utils"

export default {
    components: { FormSearch, QueryTable },
    setup() {
        const store = useStore()
        const router = useRouter()
        const route = useRoute()

        // Get last URL parameter
        const getTabFromUrl = () => {
            const regex = /\//g
            const result = route.path.replace(regex, " ").trim().split(" ")
            return result[result.length -1]
        }

        const setStateFromUrl = () => {
            const routeArgs = route.query
            const routerResult = {
                dateRange: routeArgs.start_date ?
                    [
                        convertDateToUtc(String(routeArgs.start_date)),
                        convertDateToUtc(String(routeArgs.end_date))
                    ] : null,
                searchText: routeArgs.content ? routeArgs.content : "",
                socialMedia:
                    Array.isArray(routeArgs.source) ? routeArgs.source :
                        routeArgs.source ? [routeArgs.source] : [],
                selectedPeople:
                    Array.isArray(routeArgs.author) ? routeArgs.author :
                        routeArgs.author ? [routeArgs.author] : [],
            }

            store.commit(
                'UPDATE_FROM_URL',
                {
                    form: { ...routerResult },
                    tab: getTabFromUrl(),
                    pageSize: Number(routeArgs?.page_size),
                    page: Number(routeArgs?.page),
                    sorter: routeArgs.sort_by && routeArgs.sort_by ?
                      { columnKey: routeArgs.sort_by, order: routeArgs.sort_order } : null
                }
            )

        }

        onBeforeMount(() => {
            setStateFromUrl()
        })

        watch(
            () => [
                store.state.form,
                store.state.tab,
                store.state.page,
                store.state.pageSize,
                store.state.sorter
            ],
            async () => {
                urlUpdateWithState()
             }
        )

        const urlUpdateWithState = async (
        ) => {
            const form = store.state.form;
            const page = store.state.page
            const pageSize = store.state.pageSize
            const sorter = store.state.sorter
            const routerResult = formatToApi(form, page, pageSize, sorter)
            const tab = store.state.tab;

            router.push({ path: `/consulta/${tab}/`, query: routerResult })
        }

        // Clean state before unmount
        onBeforeUnmount(() => {
            store.commit('CLEAN_STATE')
        })

        // Back button refresh table content
        window.onpopstate = async () => { setStateFromUrl() };
        // Forward button refresh table content
        window.history.forward = async () => { setStateFromUrl() };
    }
}

</script>

<template>
  <section class="padding-y-default col-span-12">
    <FormSearch />
    <QueryTable />
  </section>
</template>
