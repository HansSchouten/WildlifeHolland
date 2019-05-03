<template>
    <q-page id="page-map">
        <l-map
            ref="map"
            :zoom="zoom"
            :options="mapOptions"
            :class="`absolute ` + markerClass()">
            <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>

            <l-marker
                v-for="marker in markers"
                :key="marker.id"
                :lat-lng="marker.position"
                :icon="marker.icon"
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
                offset: this.tooltipOffset()
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
                    icon: this.getIcon(observation),
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
        },
        tooltipOffset () {
            if (this.hasCustomMarker()) {
                return [-4, -28]
            }
            return [0, -15]
        },
        markerClass () {
            if (this.hasCustomMarker()) {
                return 'custom-markers'
            }
            return 'default-markers'
        },
        hasCustomMarker () {
            return (!this.$route.query.specie)
        },
        getIcon (observation) {
            if (!this.hasCustomMarker()) {
                return null
            }
            let factor = observation.specieAbundance / (observation.maxSpeciesCount / 4)
            factor = Math.min(factor, 1)

            let color1 = [255, 0, 0]
            let color2 = [255, 255, 0]
            let color3 = [62, 195, 55]
            let computedColor = null
            if (factor < 0.5) {
                computedColor = this.colourGradientor(factor * 2, color2, color1)
            } else {
                computedColor = this.colourGradientor((factor - 0.5) * 2, color3, color2)
            }
            let pathFillColor = 'rgb(' + computedColor[0] + ',' + computedColor[1] + ',' + computedColor[2] + ')'
            return L.divIcon({
                html: '<svg version="1.1" class="marker" xmlns="http://www.w3.org/2000/svg"\n' +
                    'width="35px" height="35px" viewBox="0 0 512 512" xml:space="preserve">' +
                    '<g><path stroke="black" stroke-width="10" stroke-opacity="0.3" fill="' + pathFillColor + '" d="M206.549,0L206.549,0c-82.6,0-149.3,66.7-149.3,149.3c0,28.8,9.2,56.3,22,78.899l97.3,168.399c6.1,11,18.4,16.5,30,16.5\n' +
                    'c11.601,0,23.3-5.5,30-16.5l97.3-168.299c12.9-22.601,22-49.601,22-78.901C355.849,66.8,289.149,0,206.549,0z M206.549,193.4\n' +
                    'c-30,0-54.5-24.5-54.5-54.5s24.5-54.5,54.5-54.5s54.5,24.5,54.5,54.5C261.049,169,236.549,193.4,206.549,193.4z"/></g></svg>'
            })
        },
        colourGradientor (p, color1, color2) {
            let w = p * 2 - 1

            let w1 = (w + 1) / 2.0
            let w2 = 1 - w1

            return [parseInt(color1[0] * w1 + color2[0] * w2),
                parseInt(color1[1] * w1 + color2[1] * w2),
                parseInt(color1[2] * w1 + color2[2] * w2)]
        }
    }
}
</script>
