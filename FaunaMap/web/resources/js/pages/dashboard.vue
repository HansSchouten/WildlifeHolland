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
                    <q-select v-model="period" :options="periodOptions" label="Periode">
                        <template v-slot:prepend>
                            <q-icon name="event" />
                        </template>
                    </q-select>
                </div>
            </div>
        </div>
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
            period: 'Vandaag',
            periodOptions: [
                'Afgelopen uur',
                'Afgelopen 6uur',
                'Vandaag',
                'Gisteren',
                'Eergisteren',
                'Afgelopen 3 dagen',
                'Afgelopen week'
            ]
        }
    },

    mounted () {
        this.fetchObservations()
    },

    methods: {
        async fetchObservations () {
            await this.$store.dispatch('observations/fetchSpecieObservations')
        },
        getMapUrl (specieObservation) {
            return {
                name: 'map',
                query: {
                    specie: specieObservation.name,
                    date: specieObservation.date
                }
            }
        }
    }
}
</script>
