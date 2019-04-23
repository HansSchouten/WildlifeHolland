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
            // fetch observations
            await this.$store.dispatch('observations/fetchObservations')
        }
    },

    mounted () {
        this.fetchObservations()
    }
}
</script>
