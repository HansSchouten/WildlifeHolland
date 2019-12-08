<template>
    <q-page id="page-map">
        <div id="leaflet-map" class="absolute custom-markers"></div>
    </q-page>
</template>

<script>
import { mapGetters } from 'vuex'
import L from 'leaflet'

export default {
    middleware: 'auth',

    metaInfo () {
        return { title: this.$t('map') }
    },

    computed: {
        ...mapGetters({
            observations: 'observations/mapObservations',
            filterPeriod: 'observations/filterPeriod'
        })
    },

    data () {
        return {
            map: null,
            url: 'https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/{z}/{x}/{y}?access_token=' + window.config['mapbox_token'],
            attribution: '<a href="https://www.mapbox.com/map-feedback/">Mapbox</a> | <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            markers: [],
            markerLayer: L.layerGroup()
        }
    },

    mounted () {
        this.createMap()
        this.$nextTick(() => {
            this.fetchObservations()
        })
    },

    methods: {
        createMap () {
            this.map = L.map('leaflet-map', {
                gestureHandling: true,
                attributionControl: false
            })
            let attribution = {
                attribution: this.attribution
            }
            // increase font size on larger screens
            if (!L.Browser.mobile) {
                attribution.tileSize = 512
                attribution.zoomOffset = -1
            }
            // load tile layer
            L.tileLayer(this.url, attribution).addTo(this.map)
            // add markers layer
            this.map.addLayer(this.markerLayer)
        },
        async fetchObservations () {
            let payload = {
                specie: this.$route.query.specie,
                period: this.filterPeriod
            }
            await this.$store.dispatch('observations/fetchMapObservations', payload)
            this.updateMarkers()
        },
        updateMarkers () {
            let markers = []
            this.observations.forEach((observation) => {
                let marker = L.marker([observation.lat, observation.long], {
                    icon: this.getIcon(observation),
                    tooltip: observation.specieName + '<br>' + observation.timestamp
                })
                marker.bindPopup(observation.specieName + '<br>' +
                  observation.timestamp +
                  '<br><a target="_blank" href="https://waarneming.nl/observation/' +
                  observation.id +
                  '">Bekijk waarneming</a>')
                markers.push(marker)
            })
            this.markers = markers

            this.map.removeLayer(this.markerLayer)
            this.markerLayer = L.layerGroup(markers)
            this.markerLayer.addTo(this.map)

            this.updateBounds()
        },
        updateBounds () {
            let b = L.latLngBounds([this.markers.map(o => o.getLatLng())]).pad(0.1)
            this.map.fitBounds([
                [b.getNorth(), b.getEast()],
                [b.getSouth(), b.getWest()]
            ], true)
            this.map.setZoom(Math.min(this.map.getZoom(), 13))
        },
        getIcon (observation) {
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
