<template>
    <div>
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
            coordinates: null
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
        this.notify(this.$t('nearby_observation_notifications_enabled'))

        // load initial list of known observations
        await this.fetchNearbyObservations()
        this.knownNearbyObservations = this.nearbyObservations.map(observation => { return observation.id })

        while (true) {
            await this.sleep(10000)
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
                    console.log(observation.specieName + ' nearby!')
                    let text = observation.time + ' ' + observation.specieName
                    await this.notify(text)
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
        async notify (text) {
            if (Notification.permission !== 'denied') {
                Notification.requestPermission(function (permission) {
                    if (!('permission' in Notification)) {
                        Notification.permission = permission
                    }
                    if (permission === 'granted') {
                        new Notification(text)
                    }
                })
            }
        }
    }
}
</script>
