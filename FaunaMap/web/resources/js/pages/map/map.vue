<template>
    <q-page id="page-map">
        <l-map ref="map" :zoom="zoom" :center="center" :bounds="bounds" class="absolute">
            <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
            <l-marker
                v-for="marker in markers"
                :key="marker.id"
                :lat-lng="marker.position">
                <l-popup :content="marker.tooltip" />
                <l-tooltip :content="marker.tooltip" />
            </l-marker>
        </l-map>
    </q-page>
</template>

<script>
import { mapGetters } from 'vuex'
import { LMap, LTileLayer, LMarker, LTooltip, LPopup } from 'vue2-leaflet'

export default {
    middleware: 'auth',
    components: { LMap, LTileLayer, LMarker, LTooltip, LPopup },

    metaInfo () {
        return { title: this.$t('map') }
    },

    computed: {
        ...mapGetters({
            observations: 'observations/observations'
        })
    },

    data () {
        return {
            zoom: 13,
            center: [0, 0],
            url: 'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
            attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>',
            markers: [],
            bounds: null
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
            this.updateMarkers()
        },
        updateMarkers () {
            let markers = []
            this.observations.forEach((observation) => {
                markers.push({
                    id: observation.id,
                    position: { lat: observation.lat, lng: observation.long },
                    tooltip: ''
                })
            })
            console.log(markers)
            this.markers = markers
            this.updateBounds()
        },
        updateBounds () {
            this.bounds = window.L.latLngBounds([this.markers.map(o => o.position)])
            this.$refs.map.fitBounds([
                [51.9902, 4.5696],
                [51.9877, 4.5646]
            ])
        }
    }
}
</script>
