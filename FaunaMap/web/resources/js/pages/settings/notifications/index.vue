<template>
    <div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    middleware: 'auth',

    metaInfo () {
        return { title: this.$t('notfications') }
    },

    data () {
        return {
            knownNearbyObservations: []
        }
    },

    computed: {
        ...mapGetters({
            nearbyObservations: 'observations/nearbyObservations',
            filterPeriods: 'observations/filterPeriods'
        })
    },

    async mounted () {
        await this.fetchNearbyObservations()
        this.knownNearbyObservations = this.nearbyObservations.map(observation => { return observation.id })
        await this.sleep(10000)

        while (true) {
            await this.notifyNewNearbySightings()
            await this.sleep(10000)
        }
    },
    methods: {
        async notifyNewNearbySightings () {
            await this.fetchNearbyObservations()
            // check the loaded observations and notify any new sightings
            this.nearbyObservations.forEach(observation => {
                if (!(this.knownNearbyObservations.includes(observation.id))) {
                    console.log(observation.specieName)
                    this.notify(observation.specieName)
                }
            })
            // update the list of known nearby observations
            this.knownNearbyObservations = this.nearbyObservations.map(observation => { return observation.id })
        },
        async fetchNearbyObservations () {
            let payload = {
                period: this.filterPeriods[1]
            }
            await this.$store.dispatch('observations/fetchNearbyObservations', payload)
        },
        sleep (ms) {
            return new Promise(resolve => setTimeout(resolve, ms))
        },
        async notify (text) {
            navigator.serviceWorker.register('/sw.js')
            Notification.requestPermission(function (result) {
                if (result === 'granted') {
                    navigator.serviceWorker.ready.then(function (registration) {
                        registration.showNotification(text)
                    })
                }
            })
        }
    }
}
</script>
