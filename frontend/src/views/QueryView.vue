<script lang="ts">
import FormSearch from "../components/FormSearch.vue"
import QueryTable from "../components/QueryTable.vue"
import { onBeforeUnmount, onMounted, watch, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import { formatToApi, convertDateToUtc } from "../utils"

export default {
    components: { FormSearch, QueryTable },
    setup() {
        const store = useStore()
        const router = useRouter()      
        const route = useRoute()

        const getTabFromUrl = () => {
            return route.path.replace(/\//g, " ").trim().split(" ").pop()
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
                    page: Number(routeArgs?.page)
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
                store.state.pageSize
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
            const routerResult = formatToApi(form, page, pageSize)
            const tab = store.state.tab;

            router.push({ path: `/consulta/${tab}/`, query: routerResult })
        }
        // Clean state before unmount
        onBeforeUnmount(() => {
            store.commit('CLEAN_STATE')
        })

    }
}

</script>

<template>
    <FormSearch />
    <QueryTable />
</template>