<template>
    <div id="page-dashboard">
        <div class="q-pl-md q-pr-md q-pb-md">
            <div class="row">
                <div class="col-6 q-pr-sm">
                    <q-input v-model="term" label="Soortnaam">
                        <template v-slot:prepend>
                            <q-icon name="search" />
                        </template>
                    </q-input>
                </div>
                <div class="col-6 q-pl-sm">
                    <q-select
                        v-model="period"
                        :options="periodOptions"
                        option-value="id"
                        option-label="text"
                        label="Periode"
                        @input="fetchObservations()">
                        <template v-slot:prepend>
                            <q-icon name="event" />
                        </template>
                    </q-select>
                </div>
            </div>
        </div>
        <q-pull-to-refresh @refresh="refresher">
            <q-list id="observation-list">
                <q-item clickable v-ripple v-for="(observation, index) in observations" :key="`observation-${index}`" :to="getMapUrl(observation)">
                    <q-item-section avatar>
                        <q-avatar>
                            <img :src="observation.specieImage">
                        </q-avatar>
                    </q-item-section>
                    <q-item-section>
                        <span class="specie-name">
                            {{ observation.name }}
                        </span>
                        <span class="observation-details">
                            <span class="detail">
                                <q-icon name="fab fa-sistrix" /> {{ observation.provinces }}
                            </span>
                            <span class="detail">
                                <q-icon name="far fa-comment" /> {{ observation.count }} {{ $tc('observation', observation.count) }}
                            </span>
                            <span class="detail" v-if="observation.lastObservationTime != null">
                                <q-icon name="far fa-clock" /> {{ observation.lastObservationTime }}
                            </span>
                        </span>
                    </q-item-section>
                </q-item>
            </q-list>
        </q-pull-to-refresh>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    middleware: 'auth',

    metaInfo () {
        return { title: this.$t('dashboard') }
    },

    computed: mapGetters({
        observations: 'observations/specieObservations'
    }),

    data () {
        return {
            term: null,
            period: { id: '24', text: 'Afgelopen 24uur' },
            periodOptions: [
                { id: '1', text: 'Afgelopen uur' },
                { id: '3', text: 'Afgelopen 3uur' },
                { id: '12', text: 'Afgelopen 12uur' },
                { id: '24', text: 'Afgelopen 24uur' },
                { id: '48', text: 'Afgelopen 2 dagen' },
                { id: '72', text: 'Afgelopen 3 dagen' },
                { id: '168', text: 'Afgelopen week' }
            ]
        }
    },

    mounted () {
        this.fetchObservations()
    },

    methods: {
        async fetchObservations () {
            let payload = {
                period: this.period
            }
            await this.$store.dispatch('observations/fetchSpecieObservations', payload)
        },
        getMapUrl (specieObservation) {
            return {
                name: 'map',
                query: {
                    specie: specieObservation.name,
                    date: specieObservation.date
                }
            }
        },
        async refresher (done) {
            await this.fetchObservations()
            done()
        }
    }
}
</script>
