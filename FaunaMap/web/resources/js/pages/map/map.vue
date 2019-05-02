<template>
    <q-page id="page-map">
        <l-map
            ref="map"
            :zoom="zoom"
            :options="mapOptions"
            class="absolute">
            <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>

            <l-marker
                v-for="marker in markers"
                :key="marker.id"
                :lat-lng="marker.position"
                @click="markerClicked(marker)">

                <l-tooltip
                    :options="tooltipOptions"
                    v-if="$q.platform.is.desktop"
                    :content="marker.tooltip" />

                <l-popup :content="marker.popup" />
            </l-marker>

        </l-map>
    </q-page>
</template>

<script>
import { mapGetters } from 'vuex'
import L from 'leaflet'
import { LMap, LTileLayer, LMarker, LTooltip, LPopup } from 'vue2-leaflet'

export default {
    middleware: 'auth',
    components: { LMap, LTileLayer, LMarker, LTooltip, LPopup },

    metaInfo () {
        return { title: this.$t('map') }
    },

    computed: {
        ...mapGetters({
            observations: 'observations/mapObservations'
        })
    },

    data () {
        return {
            map: null,
            zoom: null,
            mapOptions: {
                zoomControl: false,
                attributionControl: false,
                zoomSnap: false
            },
            tooltipOptions: {
                direction: 'top',
                offset: [0, -15]
            },
            url: 'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
            attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>',
            markers: []
        }
    },

    mounted () {
        this.$nextTick(() => {
            this.fetchObservations()
            this.map = this.$refs.map
            this.map.mapObject.on('moveend', () => {
                this.zoom = this.map.mapObject.getZoom()
            })
        })
    },

    methods: {
        async fetchObservations () {
            let payload = {
                specie: this.$route.query.specie,
                date: this.$route.query.date
            }
            await this.$store.dispatch('observations/fetchMapObservations', payload)
            this.updateMarkers()
        },
        updateMarkers () {
            let markers = []
            this.observations.forEach((observation) => {
                markers.push({
                    id: observation.id,
                    position: { lat: observation.lat, lng: observation.long },
                    tooltip: observation.specieName + '<br>' + observation.timestamp,
                    popup: observation.specieName + '<br>' +
                        observation.timestamp +
                        '<br><a target="_blank" href="https://waarneming.nl/observation/' +
                        observation.id +
                        '">Bekijk waarneming</a>'
                })
            })
            this.markers = markers
            this.updateBounds()
        },
        updateBounds () {
            let b = L.latLngBounds([this.markers.map(o => o.position)]).pad(0.1)
            this.map.fitBounds([
                [b.getNorth(), b.getEast()],
                [b.getSouth(), b.getWest()]
            ], true)
            this.zoom = Math.min(this.zoom, 13)
        },
        markerClicked (marker) {
        }
    }
}
</script>
