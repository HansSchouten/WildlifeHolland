<template>
    <div id="page-map">
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    middleware: 'auth',

    metaInfo () {
        return { title: this.$t('map') }
    },

    computed: mapGetters({
        observations: 'observations/observations'
    }),

    methods: {
        async fetchObservations () {
            // get observation filter from query parameters
            let payload = {
                specie: this.$route.query.specie,
                date: this.$route.query.date
            }
            // fetch observations
            await this.$store.dispatch('observations/fetchObservations', payload)
        }
    },

    mounted () {
        this.fetchObservations()
    }
}
</script>
