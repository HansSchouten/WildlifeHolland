<template>
    <q-pull-to-refresh @refresh="refresher">
        <q-page>
            <div id="page-dashboard">
                <div class="q-pl-md q-pr-md q-pb-md">
                    <div class="row">
                        <div class="col-6 q-pr-sm">
                            <q-input
                                v-model="term"
                                label="Soortnaam"
                                @input="changeTerm">
                                <template v-slot:prepend>
                                    <q-icon name="search" />
                                </template>
                            </q-input>
                        </div>
                        <div class="col-6 q-pl-sm">
                            <q-select
                                :value="filterPeriod"
                                :options="filterPeriods"
                                option-value="id"
                                option-label="text"
                                label="Periode"
                                @input="changePeriod">
                                <template v-slot:prepend>
                                    <q-icon name="event" />
                                </template>
                            </q-select>
                        </div>
                    </div>
                </div>
                <q-list id="observation-list">
                    <q-item clickable v-ripple v-for="(observation, index) in termFilteredObservations" :key="`observation-${index}`" :to="getMapUrl(observation)">
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
            </div>
        </q-page>
    </q-pull-to-refresh>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    middleware: 'auth',

    metaInfo () {
        return { title: this.$t('dashboard') }
    },

    computed: {
        ...mapGetters({
            observations: 'observations/specieObservations',
            filterPeriods: 'observations/filterPeriods',
            filterPeriod: 'observations/filterPeriod'
        })
    },

    data () {
        return {
            term: null,
            termFilteredObservations: []
        }
    },

    mounted () {
        this.fetchObservations()
    },

    methods: {
        async fetchObservations () {
            let payload = {
                period: this.filterPeriod
            }
            await this.$store.dispatch('observations/fetchSpecieObservations', payload)
            this.termFilteredObservations = this.applyTermFilter(this.observations)
        },
        getMapUrl (specieObservation) {
            return {
                name: 'map',
                query: {
                    specie: specieObservation.name
                }
            }
        },
        async refresher (done) {
            await this.fetchObservations()
            done()
        },
        async changePeriod (newValue) {
            await this.$store.dispatch('observations/updateFilterPeriod', newValue)
            this.fetchObservations()
        },
        changeTerm () {
            this.termFilteredObservations = this.applyTermFilter(this.observations)
        },
        applyTermFilter (observations) {
            let filteredObservations = {}
            for (let specieName in observations) {
                if (!this.term || observations[specieName].name.toLowerCase().includes(this.term.toLowerCase())) {
                    filteredObservations[specieName] = observations[specieName]
                }
            }
            return filteredObservations
        }
    }
}
</script>
