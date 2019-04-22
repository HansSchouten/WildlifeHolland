<template>
    <div id="page-dashboard">
        <q-list id="observation-list">
            <q-item clickable v-ripple v-for="(observation, index) in observations" :key="`observation-${index}`">
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
                            <q-icon name="far fa-comment" /> {{ observation.count }} {{ $tc('observation', observation.count) }}
                        </span>
                        <span class="detail">
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
        observations: 'observations/observations'
    }),

    methods: {
        async fetchObservations () {
            // fetch observations
            await this.$store.dispatch('observations/fetchObservations')
        }
    },

    mounted () {
        this.fetchObservations()
    }
}
</script>
