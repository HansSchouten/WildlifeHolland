<template>
    <div class="q-pa-md">
        <q-list bordered>

            <q-item clickable v-ripple v-for="(observation, index) in observations" :key="`observation-${index}`">
                <q-item-section avatar>
                    <q-avatar>
                        <img :src="observation.specieImage">
                    </q-avatar>
                </q-item-section>
                <q-item-section>
                    {{ observation.name }}
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
    data () {
        return {
            text: ''
        }
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
