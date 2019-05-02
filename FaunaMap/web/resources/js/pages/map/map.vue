<template>
    <q-page id="page-map">
        <l-map :zoom="zoom" :center="center" class="absolute">
            <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
            <l-marker :lat-lng="marker"></l-marker>
        </l-map>
    </q-page>
</template>

<script>
import { mapGetters } from 'vuex'
import { LMap, LTileLayer, LMarker } from 'vue2-leaflet'

export default {
    middleware: 'auth',
    components: { LMap, LTileLayer, LMarker },

    metaInfo () {
        return { title: this.$t('map') }
    },

    computed: {
        ...mapGetters({
            observations: 'observations/observations'
        }),
        observationMarkers: () => {
            return []
        }
    },

    data () {
        return {
            zoom: 13,
            url: 'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
            attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>',
            markers: this.observationMarkers
        }
    },

    mounted () {
        this.fetchObservations()
    },

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
    }
}
</script>
