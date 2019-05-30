<template>
    <div class="q-pa-md">
        <q-banner class="bg-grey-3" v-if="showBanner">
            <template v-slot:avatar>
                <q-icon name="tab" color="primary" />
            </template>
            Houdt deze pagina in een tabblad open om notificaties te ontvangen van waarnemingen binnen 20km
            <template v-slot:action>
                <q-btn flat color="primary" label="Sluiten" v-on:click="showBanner = false" />
            </template>
        </q-banner>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    middleware: 'auth',

    metaInfo () {
        return { title: this.$t('notifications') }
    },

    data () {
        return {
            knownNearbyObservations: [],
            coordinates: null,
            showBanner: true
        }
    },

    computed: {
        ...mapGetters({
            nearbyObservations: 'observations/nearbyObservations',
            filterPeriods: 'observations/filterPeriods'
        })
    },

    async mounted () {
        this.$watchLocation({
            enableHighAccuracy: true,
            timeout: Infinity,
            maximumAge: 0
        }).then(c => { this.coordinates = c.lat + ',' + c.lng })

        // send test notification
        this.notify(this.$t('nearby_observation_notifications_enabled'), null)

        // load initial list of known observations
        await this.fetchNearbyObservations()
        this.knownNearbyObservations = this.nearbyObservations.map(observation => { return observation.id })

        while (true) {
            await this.sleep(20000)
            await this.notifyNewNearbySightings()
        }
    },
    methods: {
        async notifyNewNearbySightings () {
            await this.fetchNearbyObservations()

            // check the loaded observations and notify any new sightings
            for (let i = 0; i < this.nearbyObservations.length; i++) {
                let observation = this.nearbyObservations[i]
                if (!(this.knownNearbyObservations.includes(observation.id))) {
                    await this.notifyObservation(observation)
                }
            }

            // update the list of known nearby observations
            this.knownNearbyObservations = this.nearbyObservations.map(observation => { return observation.id })
        },
        async fetchNearbyObservations () {
            let payload = {
                period: this.filterPeriods[1],
                coordinates: this.coordinates,
                range: '20km'
            }
            await this.$store.dispatch('observations/fetchNearbyObservations', payload)
        },
        sleep (ms) {
            return new Promise(resolve => setTimeout(resolve, ms))
        },
        async notifyObservation (observation) {
            let text = observation.specieName

            // add time
            if (observation.timestamp.toString().includes(' ')) {
                let timestampParts = observation.timestamp.toString().split(' ')
                text = '[' + timestampParts[1] + '] ' + text
            }

            // add distance
            if (this.coordinates !== null) {
                let distance = this.geoDistance(this.coordinates, observation.location)
                let distanceText = Math.round(distance / 1000) + 'm'
                if (distance >= 1 && distance < 5) {
                    distanceText = Number(distance.toFixed(2)) + 'km'
                } else if (distance >= 5 && distance < 10) {
                    distanceText = Number(distance.toFixed(1)) + 'km'
                } else if (distance >= 10) {
                    distanceText = Math.round(distance) + 'km'
                }
                text += ' op ' + distanceText
            }

            console.log(text)
            let link = 'https://waarneming.nl/observation/' + observation.id
            await this.notify(text, link)
        },
        async notify (text, link) {
            if (Notification.permission !== 'denied') {
                Notification.requestPermission(function (permission) {
                    if (!('permission' in Notification)) {
                        Notification.permission = permission
                    }
                    if (permission === 'granted') {
                        let notification = new Notification(text)
                        if (link !== null) {
                            notification.onclick = event => {
                                event.preventDefault()
                                window.open(link, '_blank')
                            }
                        }
                    }
                })
            }
        },
        geoDistance (pos1, pos2) {
            let lat1 = pos1.split(',')[0]
            let lon1 = pos1.split(',')[1]
            let lat2 = pos2.split(',')[0]
            let lon2 = pos2.split(',')[1]

            if ((lat1 === lat2) && (lon1 === lon2)) {
                return 0
            }
            let radlat1 = Math.PI * lat1 / 180
            let radlat2 = Math.PI * lat2 / 180
            let theta = lon1 - lon2
            let radtheta = Math.PI * theta / 180
            let dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta)
            if (dist > 1) {
                dist = 1
            }
            dist = Math.acos(dist)
            dist = dist * 180 / Math.PI
            dist = dist * 60 * 1.1515
            dist = dist * 1.609344
            return dist
        }
    }
}
</script>
